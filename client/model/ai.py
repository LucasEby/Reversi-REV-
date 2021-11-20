from client.model.player import Player
from client.model.user import User


class AI(Player):
    def __init__(self, user: User, player_num: int) -> None:
        """
        Create an AI that can play as a player
        :param user: User info that the AI should inherit
        :param player_num: Play order of AI
        """
        super().__init__(user=user, player_num=player_num)
        self._difficulty = 0

    def set_difficulty(self, difficulty: int) -> None:
        """
        Set the difficulty level of the AI
        :param difficulty: Difficulty level (>0)
        """
        self._difficulty = difficulty
        self._difficulty = max(0, self._difficulty)

    def get_difficulty(self) -> int:
        """
        Returns the current difficulty level of the AI
        :return: Difficulty
        """
        return self._difficulty
