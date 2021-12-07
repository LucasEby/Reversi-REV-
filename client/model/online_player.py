from typing import Optional, Tuple

from client.model.user import User
from client.model.game import Game
from client.model.player import Player


class OnlinePlayer(Player):
    def __init__(
        self,
        user: User = None,
    ) -> None:
        super().__init__(user=user)

    def place_tile(self, game: Game) -> None:
        """
        This allows the player to place a tile. (We had to add this functionality
        after adding the AI).
        """
        game.place_tile(self.__next_move)
