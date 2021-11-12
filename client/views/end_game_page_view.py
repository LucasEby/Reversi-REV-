import string
import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class EndGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(self, game_obj: Game,
       # rematch_cb: Callable[],
       # play_again_cb: Callable[],
        play_different_mode_cb: Callable[[int], None],
    ) -> None:
        """
        
        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        self._game_obj: Game = game_obj
        super().__init__()

        
    def handle_rematch_callback():
        pass


    def display_winner(self) -> None:
        """
        Prints out the winner of the game.
        """
        winner_string: string = str(self._game_obj.get_winner())
        
