from client.model.user import User


class Player:
    def __init__(self, user: User, player_num: int) -> None:
        self._user: User = user
        # else, create an AI player
        if (player_num != 1) and (player_num != 2):
            raise Exception("Player num must be valid (1 or 2)")
        self._player_num: int = player_num

    def get_user(self) -> User:
        """
        Returns the user of the player
        :return: User
        """
        return self._user
