from abc import ABC, abstractmethod
from client.model.board import Board
from typing import Tuple


class AbstractRule(ABC):
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def is_valid_move(plyr_num: int, posn: Tuple[int, int], brd: Board) -> bool:
        """
        Determines if a move that was played is valid based on a given ruleset

        :param plyr_num: Player number of the player attempting to place a disk
        :param posn: Position of the move that is being evaluated
        :param brd: Current board
        :raises error: None
        :return: Whether a move was valid, True, or not, False
        """
        pass

    def __str__(self) -> str:
        return "AbstractRule"
