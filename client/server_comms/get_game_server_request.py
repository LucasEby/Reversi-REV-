from typing import Optional

from client.model.account import Account
from client.model.ai import AI
from client.model.game import Game
from client.model.user import User
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import get_game_server_schema


class GetGameServerRequest(BaseServerRequest):
    def __init__(self, game_id: int) -> None:
        """
        Creates server request for getting a game
        """
        super().__init__()
        self._response_schema = get_game_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["game_id"] = game_id

    def is_response_success(self) -> Optional[bool]:
        """
        Returns whether the response was a success
        :return: True if success, false if failure, None if response is expected but hasn't arrived yet
        """
        if self._response_success is None:
            return None
        elif self._response_success is False:
            return False
        else:
            return self._response_message["success"]

    def get_game_id(self) -> Optional[int]:
        """
        Retrieves game from the server response if available
        :return: Game if available, None otherwise
        """
        if self.is_response_success() is True:
            game_id: int = self._response_message["game_id"]
            # TODO how do we go from account id to user/player in a game?
            # TODO how do we create a new Game object from the retrieved data?
            saved_game: Game = Game()
            return saved_game
        else:
            return None
