from abc import ABC, abstractmethod
from client.model.board import Board
from typing import Tuple, List
import string


class AbstractRules(ABC):
    def __init__(self, name_string: string) -> None:
        """
        constructs a rules object

        :param :
        :raises error: None
        :return: None
        """
        self.name: string = name_string

    @abstractmethod
    def __is_valid_move(self, plyr_num: int, posn: Tuple[int, int], brd: Board) -> bool:
        """
        determines if a move that was played is valid based on a given ruleset

        :param plyr_num: the player number of the player attempting to place a disk
        :param posn: the position of the move that is being evaluated
        :param brd: current board state
        :raises error: None
        :return: Whether a move was valid, True, or not, False
        """
        # check flip oppenent tiles function for data
        pass
