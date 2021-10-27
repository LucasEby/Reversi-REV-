from enum import Enum


class Cell(Enum):
    empty = 0
    player1 = 1
    player2 = 2

    def flip(self) -> int:
        """
        Get the new Cell state from a flip. If the Cell has player1, return player2 and vice versa.
        If the cell is empty, don't change it.

        :return: the new Cell state
        """
        if self == Cell.player1:
            return 2
        elif self == Cell.player2:
            return 1
        else:
            return self.value

    def fill(self, curr_player: int) -> int:
        """
        Fill the empty Cell with the player indicated by curr_player. If the cell is not empty or curr_player is
        not 1 or 2, don't change it.

        :param curr_player: the player whose turn is in progress, either 1 or 2
        :return: the new Cell state
        """
        if (self == Cell.empty) & (curr_player == 1):
            return 1
        elif (self == Cell.empty) & (curr_player == 2):
            return 2
        else:
            return self.value
