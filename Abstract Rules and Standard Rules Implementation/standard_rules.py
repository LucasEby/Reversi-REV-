from abstract_rules import AbstractRules
from typing import Tuple, List
from client.model.board import Board

def __is_valid_move(self, plyr_num: int, posn: Tuple[int, int], brd: Board) -> bool:
        """
        Determines if a move that was played is valid based on the given ruleset

        :param ply_num: the number of players in the game
        :param posn: the position of the move that is being evaluated
        :param brd: current board state
        :raises error: None
        :return: Whether a move was valid, True, or not, False
        """
        # Iterate through positions in all direction
        dir_iterators = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        #generates a list of tuples that are the used to find the cells surrounding a given cell
        dir_iterators.remove((0, 0))
        #remove the tuple representing the current cell under inspection's location
        
        for dir in dir_iterators:
            # Check next cell is opposite player's
            if brd.is_valid_posn(posn[0], posn[1]) and brd.state[posn[0] + dir[0]][posn[1] + dir[1]].state != self._opposite_cell_state(plyr_num):
                continue
            x, y = posn
            # Use direction iterator to traverse board. Move is valid if same player disk is reached before edge of board or empty cell
            while brd.is_valid_posn(x, y) and brd.state[x][y].state != 0:
                if brd.state[x][y].state == self._player_cell_state(plyr_num):
                    return True
                x += dir[0]
                y += dir[1]
        return False
        