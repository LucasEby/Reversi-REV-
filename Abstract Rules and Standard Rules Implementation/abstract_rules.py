
from abc import ABC, abstractmethod
#from client.model.player import Player
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
        pass

    def __is_valid_move(plyr_num: int, posn: Tuple[int, int], brd: Board):
        """
        determines if a move that was played is valid based on a given ruleset

        :param ply_num:the number of players in the game
        :param posn: the position of the move that is being evaluated
        :param brd: current board state
        :raises error: None
        :return: Whether a move was valid, True, or not, False
        """
        #check flip oppenent tiles function for data
        pass