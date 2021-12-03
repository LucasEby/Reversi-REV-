from typing import Optional

from client.model.user import User


class Player:
    def __init__(self, player_num: int, user: Optional[User] = None) -> None:
        self._user: Optional[User] = user
        # Else, create an AI player
        if (player_num != 1) and (player_num != 2):
            raise Exception("Player num must be valid (1 or 2)")
        self._player_num: int = player_num

    def get_user(self) -> Optional[User]:
        """
        Returns the user of the player
        :return: User or None if the Player isn't also a User
        """
        return self._user
