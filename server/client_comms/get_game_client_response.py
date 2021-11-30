from threading import Condition
from typing import Dict, Any, Optional

from common.client_server_protocols import get_game_server_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import (
    DatabaseManager,
    DatabaseGame,
    DatabaseAccount,
)


class GetGameClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that gets a saved game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_get_game_success: Optional[bool] = None
        self._db_get_p1_success: Optional[bool] = None
        self._db_get_p2_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dbg: Optional[DatabaseGame] = None
        self._retrieved_p1: Optional[DatabaseAccount] = None
        self._retrieved_p2: Optional[DatabaseAccount] = None

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """

        DatabaseManager().get_game(
            callback=self.__game_retrieved_callback,
            key=self._sent_message["account_id"],
            last_game=True,
            get_game_id=True,
            get_complete=True,
            get_board_state=True,
            get_rules=True,
            get_next_turn=True,
            get_p1_account_id=False
            if "resume_game" not in self._sent_message
            else self._sent_message["resume_game"],
            get_p2_account_id=False
            if "resume_game" not in self._sent_message
            else self._sent_message["resume_game"],
            get_ai_difficulty=False
            if "resume_game" not in self._sent_message
            else self._sent_message["resume_game"],
        )

        # Wait for database to complete task
        with self._db_complete_cv:
            while self._db_get_game_success is None:
                self._db_complete_cv.wait()

        if (
            "resume_game" in self._sent_message
            and self._sent_message["resume_game"]
            and self._retrieved_dbg is not None
        ):
            # Get user info from database
            DatabaseManager().get_account(
                callback=self.__p1_retrieved_callback,
                key=self._retrieved_dbg.p1_account_id,
                get_username=True,
                get_elo=True,
            )
            DatabaseManager().get_account(
                callback=self.__p2_retrieved_callback,
                key=self._retrieved_dbg.p2_account_id,
                get_username=True,
                get_elo=True,
            )
            # Wait for database to complete task
            with self._db_complete_cv:
                while (
                    self._db_get_p1_success is None or self._db_get_p2_success is None
                ):
                    self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "protocol_type": get_game_server_schema.schema["protocol_type"],
                "success": self._db_get_game_success,
                "game_id": 0
                if self._retrieved_dbg is None
                else self._retrieved_dbg.game_id,
                "complete": None
                if self._retrieved_dbg is None
                else self._retrieved_dbg.complete,
                "board_state": [[0]]
                if self._retrieved_dbg is None
                else self._retrieved_dbg.board_state,
                "rules": ""
                if self._retrieved_dbg is None
                else self._retrieved_dbg.rules,
                "next_turn": 0
                if self._retrieved_dbg is None
                else self._retrieved_dbg.next_turn,
            }
        )
        if (
            self._retrieved_dbg is not None
            and self._retrieved_dbg.ai_difficulty is not None
        ):
            self._response_message.update(
                {"ai_difficulty": self._retrieved_dbg.ai_difficulty}
            )
        if (
            "resume_game" in self._sent_message
            and self._sent_message["resume_game"]
            and self._retrieved_dbg is not None
        ):
            self._response_message.update(
                {
                    "accounts": {
                        "p1_account_id": self._retrieved_dbg.p1_account_id,
                        "p1_username": ""
                        if self._retrieved_p1 is None
                        else self._retrieved_p1.username,
                        "p1_elo": 0
                        if self._retrieved_p1 is None
                        else self._retrieved_p1.elo,
                        "p2_account_id": self._retrieved_dbg.p2_account_id,
                        "p2_username": ""
                        if self._retrieved_p2 is None
                        else self._retrieved_p2.username,
                        "p2_elo": 0
                        if self._retrieved_p2 is None
                        else self._retrieved_p2.elo,
                    }
                }
            )
        else:
            self._response_message.update(
                {
                    "accounts": None,
                }
            )
        return self._response_message

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

    def __p1_retrieved_callback(self, success: bool, dba: DatabaseAccount) -> None:
        """
        Callback for when the account has finished being received from the Database Manager
        :param success: Whether retrieval was successful or not
        :param dba: Database account retrieved from database
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_account_success = success
            if success is True:
                self._retrieved_p1 = dba
            self._db_complete_cv.notify()

    def __p2_retrieved_callback(self, success: bool, dba: DatabaseAccount) -> None:
        """
        Callback for when the account has finished being received from the Database Manager
        :param success: Whether retrieval was successful or not
        :param dba: Database account retrieved from database
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_account_success = success
            if success is True:
                self._retrieved_p2 = dba
            self._db_complete_cv.notify()
