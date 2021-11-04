from enum import Enum


class CellState(Enum):
    empty = 0
    player1 = 1
    player2 = 2


class Cell:
    state: CellState = CellState.empty

    def __init__(self, state: CellState):
        self.state = state

    def flip(self) -> None:
        """
        Flip the Cell state from 1 to 2 or 2 to 1. If the cell is empty, don't change it.
        """
        if self.state.value == 1:
            self.state = CellState.player2
        elif self.state.value == 2:
            self.state = CellState.player1

    def fill(self, curr_player: int) -> None:
        """
        Fill the empty Cell with the player indicated by curr_player. If the cell is not empty don't change it.

        :param curr_player: the player whose turn is in progress, either 1 or 2
        """
        if self.state.value == 0:
            self.state = CellState(curr_player)
