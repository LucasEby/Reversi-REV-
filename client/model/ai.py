from typing import Tuple, List
import math
import copy

from numpy import Infinity

from client.model.player import Player
from client.model.game import Game
from client.model.cell import CellState
from client.model.user import User
from client.model.game_manager import GameManager


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

        :return: an integer difficulty
        """
        return self._difficulty

    def place_tile(self, game: Game) -> None:
        """
        This allows the AI to place a tile. (We had to add this functionality
        after adding the AI).

        param: game is the game object that the AI will place it's tile on.
        """
        game.place_tile(self.__get_move(game=game))

    def __weight_pos(self, row: int, col: int, game: Game) -> int:
        """
        This function is used to weight the end node of the tree.

        param: row is the row of the position that the user wants to weight.
        param: col is the column of the position that the user wants to weight.
        param: game is the game object that the user would like to get the position's weight for.
        return: an integer number that represents the weight of the position.
        """

        board_size = game.board.size
        half: int = math.floor(board_size / 2)

        # position_weight: weight of the position chosen as a result of its location on the board
        if ((row == 0) and ((col == 0) or (col == board_size - 1))) or (
            (row == board_size - 1) and ((col == 0) or (col == board_size - 1))
        ):
            # position is located in the corner.
            position_weight = 4
        elif ((row <= 1) and ((col <= 1) or (col >= board_size - 2))) or (
            (row >= board_size - 2) and ((col <= 1) or (col >= board_size - 2))
        ):
            # position is located next to a corner. This is THE WORST POSITION.
            position_weight = -4
        elif (
            (row == 0)
            or (row == board_size - 1)
            or (col == 0)
            or (col == board_size - 1)
        ):
            # position is located on an edge. It is not a corner and is not next to a corner.
            position_weight = 3
        elif ((row >= half - 1) or (row <= half)) and (
            (col >= half - 1) or (col <= half)
        ):
            # position is located in the 4 middle cells in the center of the board.
            position_weight = 2
        else:
            # position is located somewhere else on the board.
            position_weight = 1

        """
        # This is in case we want to add the score as additional weight to the position:
        # This variable is in case we need to scale the position_weight:
        position_weight = position_weight * 10
        score = game.get_score()
        weighted_score = score[0] - score[1]
        position_weight = position_weight + weighted_score
        """
        return position_weight

    def __get_move(self, game: Game) -> Tuple[int, int]:
        """
        This function is used to return the AI's calculated next move.

        param: game is the current game that the AI is playing.
        return Tuple[int, int] that represents the position that the AI will place a tile at.
        """
        bestScore = -Infinity
        board_state: List[List[CellState]] = game.board.get_state()
        valid_moves: List[List[bool]] = game.get_valid_moves()
        move: Tuple[int, int] = (0, 0)
        for row in range(0, game.board.size):
            for col in range(0, game.board.size):
                if (board_state[row][col] == CellState.empty) and valid_moves[row][col]:
                    copied_game = copy.deepcopy(game)
                    copied_game.place_tile((row, col))
                    score = self.__minimax(copied_game, 0, False)
                    if score > bestScore:
                        bestScore = score
                        move = (row, col)
        return move

    def __minimax(self, game: Game, depth: int, is_maximizing: bool) -> int:
        """
        This function is used to operate the minimax algorithm on a copy of the game.
        This function will recursively call itself to iterate through the different branches.

        param: game represents the copy of the game object that the algorithm uses to calculate its next move.
        param: depth the current location in the branches.
        param: is_maximizing is a boolean that is true if it is calculating the AI's move, false if it is
        calculating the human player's move.
        returns: an integer that represents the score of the end node.
        """
        if game.is_game_over():
            if game.get_winner() == 1:
                return math.floor(-Infinity)
            elif game.get_winner() == 2:
                return math.floor(Infinity)
            else:
                return 0

        board_state: List[List[CellState]] = game.board.get_state()
        valid_moves: List[List[bool]] = game.get_valid_moves()

        if is_maximizing:
            bestScore = math.floor(-Infinity)
            for row in range(0, game.board.size):
                for col in range(0, game.board.size):
                    # Is the spot available?
                    if (
                        (board_state[row][col] == CellState.empty)
                        and valid_moves[row][col]
                        and (depth < self._difficulty)
                    ):
                        copied_game = copy.deepcopy(game)
                        copied_game.place_tile((row, col))
                        score = self.__minimax(copied_game, depth + 1, False)
                        bestScore = max(score, bestScore)
                    elif (board_state[row][col] == CellState.empty) and valid_moves[
                        row
                    ][col]:
                        # we're at the terminal point that we want to go to.
                        score = self.__weight_pos(row=row, col=col, game=game)
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = math.floor(Infinity)
            for row in range(0, game.board.size):
                for col in range(0, game.board.size):
                    # Is the spot available?
                    if (
                        (board_state[row][col] == CellState.empty)
                        and valid_moves[row][col]
                        and (depth < self._difficulty)
                    ):
                        copied_game = copy.deepcopy(game)
                        copied_game.place_tile((row, col))
                        score = self.__minimax(copied_game, depth + 1, True)
                        bestScore = min(score, bestScore)
                    elif (board_state[row][col] == CellState.empty) and valid_moves[
                        row
                    ][col]:
                        # we're at the terminal point that we want to go to.
                        # Negative was put here on purpose:
                        score = -self.__weight_pos(row=row, col=col, game=game)
                        bestScore = max(score, bestScore)
            return bestScore


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
# scores1 = [3, 5, 2, 9, 12, 5, 23, 23]
#
# tree_depth = math.log(len(scores1), 2)
# main_user: User = User(username="P1")
# main_user.get_preference().set_board_size(8)
# player1 = Player(1)
# player2 = AI(1)
# game_manager = GameManager()
# game = Game(main_user.get_preference().get_board_size(), main_user.get_preference().get_rule(), False, False)
# ai.set_difficulty(int(tree_depth))
#
# print("The optimal value is : ", end="")
# print(ai.minimax(0, 0, True, scores1))
