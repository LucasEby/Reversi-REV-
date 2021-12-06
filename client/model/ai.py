from client.model.player import Player


class AI(Player):
    def __init__(self, player_num: int) -> None:
        """
        Create an AI that can play as a player
        :param player_num: Play order of AI
        """
        super().__init__(user=None, player_num=player_num)
        self._difficulty: int = 0

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty: int) -> None:
        """
        Set the difficulty level of the AI

        :param difficulty: Difficulty level (>0)
        """
        self._difficulty = max(0, difficulty)

    def get_difficulty(self) -> int:
        """
        Returns the current difficulty level of the AI

        :return: Difficulty
        """
        return self._difficulty
