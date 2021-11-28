from threading import Condition
from typing import Dict, Any, Optional

from common.client_server_protocols import get_game_server_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseGame


class GetGameClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that gets a saved game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_get_game_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dbg: Optional[DatabaseGame] = None

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """
        DatabaseManager().get_game(
            callback=self.__game_retrieved_callback,
            key=self._sent_message["game_id"],
            get_board_state=True,
            get_next_turn=True,
        )

        # Wait for database to complete task
        with self._db_complete_cv:
            while self._db_get_game_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "protocol_type": get_game_server_schema.schema["protocol_type"],
                "success": self._db_get_game_success,
                "game_id": 0
                if self._retrieved_dbg is None
                else self._retrieved_dbg.game_id,
                "board_state": [[0]]
                if self._retrieved_dbg is None
                else self._retrieved_dbg.board_state,
                "next_turn": 0
                if self._retrieved_dbg is None
                else self._retrieved_dbg.next_turn,
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
