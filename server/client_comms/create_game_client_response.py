from datetime import datetime
from socket import socket
from typing import Dict, Any, Tuple

from common.client_server_protocols import create_game_server_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.client_comms.server_comms_manager import ServerCommsManager
from server.database_management.database_manager import DatabaseManager, DatabaseGame


class CreateGameClientResponse(BaseClientResponse):

    def __init__(self, message: Dict[str, Any], connection: socket, addr: Tuple[int, int]) -> None:
        """
        C'tor for response handler that creates a new game in the database manager
        :param message: Message info from client
        :param connection: Client socket connection
        :param addr: Client return address
        """
        super().__init__(message=message, connection=connection, addr=addr)
        self._db_success: bool = False

    def handle_request(self) -> None:
        """
        Create a game in the database manager
        """
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

    def respond(self) -> None:
        """
        Respond to the client through the server comms manager
        """
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
        ServerCommsManager().send(msg=self._response_message, s=self._client_connection, addr=self._client_address)

    def __game_created_callback(self, success: bool) -> None:
        """
        Callback for when the game has finished being created in the Database Manager
        :param success: Whether game was created successfully
        """
        self._db_success = success
        self._handled = True
        self._respond_callback(self)

