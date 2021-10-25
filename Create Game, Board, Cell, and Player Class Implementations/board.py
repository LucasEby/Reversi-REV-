from enum import Enum


class Board:
    def __init__(self, size: int, next_turn: int):
        self.size: int = size
        if size % 2 != 0:
            raise Exception("Board size must be an even number")
        self.cells: Cell[size][size] = [[Cell.empty for c in range(size)] for r in range(size)]
        # initialize the four starting disks at the center of the board
        cells[size/2+1][size/2] = Cell.player1
        cells[size/2][size/2+1] = Cell.player1
        cells[size/2][size/2] = Cell.player2
        cells[size/2+1][size/2+1] = Cell.player2
        self.next_turn = next_turn

    def get_state(self) -> Cell[size][size]:
        """
        Get the current state of the board, the cells field.

        :return: cells
        """
        return cells

    def get_num_type(self, type: Cell):
        """
        Get the number of cells in the board that are of the given Cell type.

        :param type: the type of Cell to count
        :return: the number of the given Cell type cells in the board
        """
        if type == 0:
            return len(filter((cell != 1 & cell != 2), self.cells))
        elif type == 1:
            return len(filter((cell != 0 & cell != 2), self.cells))
        elif type == 2:
            return len(filter((cell != 0 & cell != 1), self.cells))


class Cell(Enum):
    player1 = 0
    player2 = 1
    empty = 2

    def flip(self) -> Cell:
        """
        Get the new Cell state from a flip. If the Cell has player1, return player2 and vice versa.
        If the cell is empty, don't change it.

        :return: the new Cell state
        """
        if self == Cell.player1:
            return Cell.player2
        elif self == Cell.player2:
            return Cell.player1
        else:
            return self

    def fill(self, curr_player: int) -> Cell:
        """
        Fill the empty Cell with the player indicated by curr_player. If the cell is not empty or curr_player is
        not 0 or 1, don't change it.

        :param curr_player: the player whose turn is in progress, either 0 or 1
        :return: the new Cell state
        """
        if self == Cell.empty & curr_player == 0:
            return Cell.player1
        elif self == Cell.empty & curr_player == 1:
            return Cell.player2
        else:
            return self
