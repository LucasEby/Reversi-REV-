from typing import Optional, Tuple

from client.model.user import User
from client.model.game import Game


class Player:
    def __init__(self, user: User = None) -> None:
        self._user: User = user
        self.__next_move: Tuple[int, int] = (0, 0)

    def get_user(self) -> User:
        """
        Returns the user of the player
        :return: User or None if the Player isn't also a User
        """
        return self._user

    def place_tile(self, game: Game) -> None:
        """
        This allows the player to place a tile. (We had to add this functionality
        after adding the AI).
        """
        game.place_tile(self.__next_move)

    def set_next_move(self, posn: Tuple[int, int]) -> None:
        self.__next_move = posn

    # Might need this?
    def get_next_move(self) -> Tuple[int, int]:
        """
        Returns the next move the player wants to play
        :return a Tuple representing the coordinates of the move.
        """
        return self.__next_move
