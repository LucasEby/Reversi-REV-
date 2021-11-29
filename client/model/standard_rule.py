from typing import Tuple, List

from client.model.abstract_rule import AbstractRule
from client.model.board import Board
from client.model.cell import CellState
from client.model.cell import Cell
from client.model.board import Board


class StandardRule(AbstractRule):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def is_valid_move(plyr_num: int, posn: Tuple[int, int], brd: Board) -> bool:
        """
        Determines if a move that was played is valid based on the given ruleset

        :param plyr_num: the player number of the player attempting to place a disk
        :param posn: the position of the move that is being evaluated
        :param game: current game state
        :return: Whether a move was valid, True, or not, False
        """
        # Verify the current cell is unoccupied
        brd_state_cells: List[List[Cell]] = brd.get_state()
        brd_state: List[List[CellState]] = []
        temp_state: List[CellState] = []
        for i in range(len(brd_state_cells)):
            for j in range(len(brd_state_cells[0])):
                temp_state.append(brd_state_cells[i][j].state)
            brd_state.append(temp_state)

        if not brd_state[posn[0]][posn[1]] == CellState.empty:
            print("THIS GOT CALLED")
            return False

        # Generates a list of tuples that are the used to find the cells surrounding a given cell
        dir_iterators = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        # Remove the tuple representing no movement
        dir_iterators.remove((0, 0))

        # Iterate through positions in all direction
        for d in dir_iterators:
            # Check next cell is opposite player's
            if brd.is_valid_posn(posn[0] + d[0], posn[1] + d[1]) and brd_state[
                posn[0] + d[0]
            ][posn[1] + d[1]] != (
                CellState.player2 if plyr_num == 1 else CellState.player1
            ):
                continue
            x, y = (posn[0] + d[0], posn[1] + d[1])
            # Use direction iterator to traverse board. Move is valid if same player disk is reached before edge of
            # board or empty cell
            while brd.is_valid_posn(x, y) and brd_state[x][y] != CellState.empty:
                if brd_state[x][y] == (
                    CellState.player1 if plyr_num == 1 else CellState.player2
                ):
                    return True
                x += d[0]
                y += d[1]
        return False

    def __str__(self) -> str:
        return "StandardRule"
