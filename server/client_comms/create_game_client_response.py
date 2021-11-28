from datetime import datetime
from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema

from common.client_server_protocols import (
    create_game_server_schema,
    create_game_client_schema,
)
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseGame


class CreateGameClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that creates a new game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_create_game_success: Optional[bool] = None
        self._db_get_game_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dbg: Optional[DatabaseGame] = None
        self._sent_message_schema: Schema = create_game_client_schema
        self._response_message_schema: Schema = create_game_server_schema
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
            self._response_message.update({"success": False, "game_id": 0})
            return self._response_message

        # Create a game in the database
        dbg: DatabaseGame = DatabaseGame(
            complete=False,
            board_state=self._sent_message["board_state"],
            rules=self._sent_message["rules"],
            next_turn=1,
            p1_account_id=None
            if "p1_account_id" not in self._sent_message
            else self._sent_message["p1_account_id"],
            p2_account_id=None
            if "p2_account_id" not in self._sent_message
            else self._sent_message["p2_account_id"],
            ai_difficulty=None
            if "ai_difficulty" not in self._sent_message
            else self._sent_message["ai_difficulty"],
            last_save=datetime.now(),
        )
        DatabaseManager().create_game(
            callback=self.__game_created_callback, database_game=dbg
        )
        account_id: str = (
            "p1_account_id"
            if "p1_account_id" in self._sent_message
            else "p2_account_id"
        )
        DatabaseManager().get_game(
            key=self._sent_message[account_id],
            callback=self.__game_retrieved_callback,
            last_game=True,
            get_game_id=True,
        )

        # Wait for database to complete tasks
        with self._db_complete_cv:
            while (
                self._db_create_game_success is None
                or self._db_get_game_success is None
            ):
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "success": self._db_create_game_success and self._db_get_game_success,
                "game_id": 0
                if self._retrieved_dbg is None
                else self._retrieved_dbg.game_id,
            }
        )
        return self._response_message

    def __game_created_callback(self, success: bool) -> None:
        """
        Callback for when the game has finished being created in the Database Manager
        :param success: Whether game was created successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_create_game_success = success
            self._db_complete_cv.notify()

    def __game_retrieved_callback(self, success: bool, dbg: DatabaseGame) -> None:
        """
        Callback for when the game has finished being received from the Database Manager
        :param success: Whether retrieval was successful or not
        :param dbg: Database game retrieved from database
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_game_success = success
            if success is True:
                self._retrieved_dbg = dbg
            self._db_complete_cv.notify()
