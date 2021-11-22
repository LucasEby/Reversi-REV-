from datetime import datetime
from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema

from common.client_server_protocols import (
    save_game_client_schema,
    save_game_server_schema,
)
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseGame


class SaveGameClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that saves an existing game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._sent_message_schema: Schema = save_game_client_schema
        self._response_message_schema: Schema = save_game_server_schema
        self._response_message["protocol_type"] = self._response_message_schema.schema[
            "protocol_type"
        ]

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        :return Message to send to client
        """
        # Check schema of incoming message is ok
        if not self._sent_message_schema.is_valid(self._sent_message):
            self._response_message["success"] = False
            return self._response_message

        # Update game in database
        dbg: DatabaseGame = DatabaseGame(
            complete=self._sent_message["complete"],
            board_state=self._sent_message["board_state"],
            next_turn=self._sent_message["next_turn"],
            last_save=datetime.now(),
        )
        DatabaseManager().update_game(
            callback=self.__game_updated_callback,
            game_id=self._sent_message["game_id"],
            database_game=dbg,
        )

        # Wait for database manager to complete task
        with self._db_complete_cv:
            while self._db_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message["success"] = self._db_success
        return self._response_message

    def __game_updated_callback(self, success: bool) -> None:
        """
        Callback for when the game has finished being saved in the database manager
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_success = success
            self._db_complete_cv.notify()
