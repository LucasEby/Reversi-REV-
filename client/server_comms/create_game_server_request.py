from typing import Optional

from client.model.account import Account
from client.model.ai import AI
from client.model.game import Game
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import create_game_server_schema


class CreateGameServerRequest(BaseServerRequest):
    def __init__(self, game: Game) -> None:
        """
        Creates server request for creating a game
        """
        super().__init__()
        self._response_schema = create_game_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["rules"] = str(game.get_rules())
        self._send_message["board_state"] = [
            [cell.value for cell in row] for row in game.board.get_state()
        ]
        if game.get_player1() is not None and isinstance(
            game.get_player1().get_user(), Account
        ):
            self._send_message["p1_account_id"] = game.get_player1().get_user().id
        if game.get_player2() is not None and isinstance(
            game.get_player2().get_user(), Account
        ):
            self._send_message["p2_account_id"] = game.get_player2().get_user().id
        if isinstance(game.get_player1(), AI):
            self._send_message["ai_difficulty"] = game.get_player1().get_difficulty()
        elif isinstance(game.get_player2(), AI):
            self._send_message["ai_difficulty"] = game.get_player1().get_difficulty()

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
        Retrieves game ID from the server response if available
        :return: Game ID if available, None otherwise
        """
        if self.is_response_success() is True:
            return self._response_message["game_id"]
        else:
            return None
