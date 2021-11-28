from typing import Optional, List

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

    def get_game(self) -> Optional[List[int, List[List[int]], int]]:
        """
        Retrieves changed game from the server response if available
        :return: New states of board and next_turn if available, None otherwise
        """
        if self.is_response_success() is True:
            game_id: int = self._response_message["game_id"]
            board_state: [[int]] = self._response_message["board_state"]
            next_turn: int = self._response_message["next_turn"]
            info: List[int, List[List[int]], int] = [game_id, board_state, next_turn]
            return info
        else:
            return None
