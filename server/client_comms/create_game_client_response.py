from datetime import datetime
from threading import Condition
from typing import Dict, Any, Optional

from common.client_server_protocols import create_game_server_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseGame


class CreateGameClientResponse(BaseClientResponse):

    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that creates a new game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """
        # Create a game in the database
        dbg: DatabaseGame = DatabaseGame(
            complete=False,
            board_state=self._sent_message["board_state"],
            rules=self._sent_message["rules"],
            next_turn=1,
            p1_account_id=None if "p1_account_id" not in self._sent_message else self._sent_message["p1_account_id"],
            p2_account_id=None if "p2_account_id" not in self._sent_message else self._sent_message["p2_account_id"],
            ai_difficulty=None if "ai_difficulty" not in self._sent_message else self._sent_message["ai_difficulty"],
            last_save=datetime.now(),
        )
        DatabaseManager().create_game(callback=self.__game_created_callback, database_game=dbg)

        # Wait for database to complete task
        with self._db_complete_cv:
            while self._db_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "protocol_type": create_game_server_schema.schema["protocol_type"],
                "success": self._db_success,
                # TODO: Set other fields of _response_message correctly
                "game_id": 0,
                "opponent": {
                    "username": "test"
                }
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
            self._db_success = success
            self._db_complete_cv.notify()

