from typing import Optional, Union, List, Dict, Any

from client.model.account import Account
from client.model.board import Board
from client.model.game import Game, UpdatedGameInfo
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import get_game_server_schema


class GetGameServerRequest(BaseServerRequest):
    def __init__(self, account_id: int, resume_game: bool) -> None:
        """
        Creates server request for getting a game from a user's ID
        """
        super().__init__()
        self._response_schema = get_game_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["account_id"] = account_id
        self._send_message["resume_game"] = resume_game

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

    def get_game(self) -> Optional[Union[Game, UpdatedGameInfo]]:
        """
        Retrieves changed game from the server response if available
        :return: New game or updated game info, None otherwise
        """
        if self.is_response_success() is True and self._send_message["resume_game"]:
            # Note: not currently using the "complete" or "ai_difficulty" fields,
            # but they are included because they may be useful
            game_id: int = self._response_message["game_id"]
            complete: bool = self._response_message["complete"]
            board_state: List[List[int]] = self._response_message["board_state"]
            size: int = len(board_state[0])
            next_turn: int = self._response_message["next_turn"]
            if "account1" in self._response_message:
                account1: Optional[Dict[str, Any]] = self._response_message["account1"]
            else:
                account1 = None
            if "account2" in self._response_message:
                account2: Optional[Dict[str, Any]] = self._response_message["account2"]
            else:
                account2 = None
            new_board: Board = Board(size, board_state)
            p1: Optional[Account] = None
            p2: Optional[Account] = None
            ai_difficulty: int = 0
            new_game: Optional[Game] = None
            if account1 is not None:
                p1_id: int = account1["p1_account_id"]
                p1_username: str = account1["p1_username"]
                p1_elo: int = account1["p1_elo"]
                p1 = Account(p1_username, p1_elo, p1_id)
            if account2 is not None:
                p2_id: int = account2["p2_account_id"]
                p2_username: str = account2["p2_username"]
                p2_elo: int = account2["p2_elo"]
                p2 = Account(p2_username, p2_elo, p2_id)
            if "ai_difficulty" in self._response_message:
                ai_difficulty = self._response_message["ai_difficulty"]
            if p1 is not None:
                new_game = Game(
                    p1, p2, save=True, saved_board=new_board, next_turn=next_turn
                )
                new_game.set_id(game_id)
            return new_game
        elif (
            self.is_response_success() is True and not self._send_message["resume_game"]
        ):
            board_state = self._response_message["board_state"]
            size = len(board_state[0])
            new_board = Board(size, board_state)
            next_turn = self._response_message["next_turn"]
            updated_info: UpdatedGameInfo = UpdatedGameInfo(new_board, next_turn)
            return updated_info
        else:
            return None
