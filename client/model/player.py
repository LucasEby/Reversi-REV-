from typing import Optional, Tuple

from client.model.user import User
from client.model.game import Game


class Player:

    def __init__(self, player_num: int, user: Optional[User] = None, player_type: Optional[str] = "local_multi") -> None:
        self._user: Optional[User] = user
        # Else, create an AI player
        if (player_num != 1) and (player_num != 2):
            raise Exception("Player num must be valid (1 or 2)")
        self._player_num: int = player_num
        self.__next_move: Tuple[int, int] = (0, 0)
        self.get_player_type = player_type
        if player_type == "local_multi":
            self._player_type = player_type
        elif player_type == "local_ai":
            self._player_type = player_type
        elif player_type == "online":
            self._player_type = player_type
        else:
            raise Exception("Player type does not exist.")

    def get_user(self) -> Optional[User]:
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
        # if isinstance(self, AI):
        #    self.__next_move = self.get_move(game)
        # else:
        # type is equal to user
        game.place_tile(self.__next_move)

    def get_move(self, game: Game):
        pass

    def set_next_move(self, posn: Tuple[int, int]) -> None:
        self.__next_move = posn

    def get_player_type(self) -> str:
        return self._player_type

    # Might need this?
    def get_next_move(self) -> Tuple[int, int]:
        """
        Returns the next move the player wants to play
        :return a Tuple representing the coordinates of the move.
        """
        return self.__next_move
