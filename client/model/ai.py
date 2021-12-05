from typing import Tuple

from client.model.player import Player
from client.model.game import Game
import math


class AI(Player):
    def __init__(self, player_num: int) -> None:
        """
        Create an AI that can play as a player
        :param player_num: Play order of AI
        """
        super().__init__(user=None, player_num=player_num)
        self._difficulty: int = 0
        self._player_type: str = "local_ai"

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

    def get_move(self, game: Game) -> None:
        return Tuple[0: int, 0: int]

    def place_tile(self, game: Game) -> None:
        """
        This allows the AI to place a tile. (We had to add this functionality
        after adding the AI).
        """
        game.place_tile(self.__next_move)
        # TODO: need to add this functionality in.

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


# AI Weight class
# 4 end conditions to check with their weight:
# Corners are the best
# Edges that are NOT next to corners are the second best
# The closer a piece is to the middle, the better it is
# Cells that are next to corners are the worst

# AI check class
# So this will have to create the tree somehow
# We'll need a function in here that'll iterate through recursively probably

# The AI difficulty is the depth it searches the tree.

# MAX - WIN
# 4 - Corner
# 3 - Edge that is not next to a corner
# 2 - The closest piece to the middle
# 1 - Cell that is next to a corner
# -4 - Corner for opponent
# -3 - Edge that is not next to a corner for opponent
# -2 - The closest piece to the middle for the opponent
# -1 - Cell that is next ot a corner for opponent
# MIN - LOSS (Opponent wins)

# need to use get

# Driver code
scores1 = [3, 5, 2, 9, 12, 5, 23, 23]

tree_depth = math.log(len(scores1), 2)

ai = AI(1)
ai.set_difficulty(int(tree_depth))

print("The optimal value is : ", end="")
print(ai.minimax(0, 0, True, scores1))
