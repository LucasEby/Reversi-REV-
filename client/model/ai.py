from client.model.player import Player
from client.model.user import User
import math


class AI(Player):
    def __init__(self, player_num: int) -> None:
        """
        Create an AI that can play as a player
        :param player_num: Play order of AI
        """
        super().__init__(user=None, player_num=player_num)
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

    def minimax(self, cur_depth, node_index,
                max_turn, scores):
        """
        Minimax algorithm that we'll use to calculate the AI decisions
        """
        target_depth = self._difficulty
        # base case : targetDepth reached
        if cur_depth == target_depth:
            return scores[node_index]

        if (max_turn):
            return max(self.minimax(cur_depth + 1, node_index * 2,
                               False, scores),
                       self.minimax(cur_depth + 1, node_index * 2 + 1,
                               False, scores))

        else:
            return min(self.minimax(cur_depth + 1, node_index * 2,
                               True, scores),
                       self.minimax(cur_depth + 1, node_index * 2 + 1,
                               True, scores))


# AI array of numbers each number will b
#

# Driver code
scores1 = [3, 5, 2, 9, 12, 5, 23, 23]

tree_depth = math.log(len(scores1), 2)

ai = AI(5)
ai.set_difficulty(int(tree_depth))

print("The optimal value is : ", end="")
print(ai.minimax(0, 0, True, scores1))
