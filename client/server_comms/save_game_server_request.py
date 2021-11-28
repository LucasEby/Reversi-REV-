from typing import Optional

from schema import Schema

from client.model.game import Game
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import save_game_server_schema


class SaveGameServerRequest(BaseServerRequest):
    def __init__(self, game: Game) -> None:
        """
        Creates server request for saving a game state
        :param game: Game to save
        """
        super().__init__()
        self._response_schema: Schema = save_game_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["game_id"] = game.get_id()
        self._send_message["complete"] = game.is_game_over()
        self._send_message["board_state"] = [
            [cell.value for cell in row] for row in game.board.get_state()
        ]
        self._send_message["next_turn"] = game.get_curr_player()

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
