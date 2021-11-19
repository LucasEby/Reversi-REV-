import string
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView
import tkinter as tk

# from PIL import Image, ImageTk


class PlayGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game_obj: Game,
        place_tile_cb: Callable[[Tuple[int, int]], None],
        forfeit_cb: Callable[[int], None],
        window,
    ) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board
        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        super().__init__(window=window)
        self._game_obj: Game = game_obj
        self._size: int = game_obj.board.size
        self._place_tile_cb = place_tile_cb
        self._forfeit_cb = forfeit_cb
        self.window = window
        self.play_game_frame = tk.Frame(self.window, padding=10)
        self.play_game_frame.grid()

    def start_gui(self):
        self.__display_board()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """

        board_state: List[List[Cell]] = self._game_obj.board.get_state()
        for row in range(0, self._size + 1):
            for col in range(0, self._size + 1):
                if board_state[row][col].state == CellState.player1:
                    tk.Label(self.play_game_frame, fg="green").grid(column=col, row=row)
                elif board_state[row][col].state == CellState.player2:
                    tk.Label(self.play_game_frame, fg="blue").grid(column=col, row=row)
                elif board_state[row][col].state == CellState.empty:
                    tk.Button(
                        self.play_game_frame,
                        fg="purple",
                        command=self.__tile_clicked(row=row, col=col),
                    ).grid(column=col, row=row)

    def __display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple: tuple = self._game_obj.get_score()
        temp_string0: string = str(temp_tuple[0])
        temp_string1: string = str(temp_tuple[1])
        print("Player 1's score: " + temp_string0)
        print("Player 2's score: " + temp_string1)

    def __tile_clicked(self, row: int, col: int) -> None:
        print("fish")
        # def __display_tile_placement(self) -> None:
        #     """
        #     Displays graphic for user to enter tile placement info
        #     """
        #     valid_input: bool = False
        #     row: int = 0
        #     col: int = 0
        #     print(f"\nPlayer {self._game_obj.curr_player}'s turn")
        #     while not valid_input:
        #         row_str: str = input("Enter row for disk: ")
        #         col_str = input("Enter col for disk: ")
        #         try:
        #             row = int(row_str) - 1
        #             col = ord(col_str.lower()) - 97
        #         except ValueError:
        #             print("Invalid row or col. Please try again.")
        #             continue
        #         valid_input = True
        #     self._place_tile_cb((row, col))

    # TODO: move display_winner into the end game view
    def display_winner(self) -> None:
        """
        Prints out the winner of the game.
        """
        winner_string: string = str(self._game_obj.get_winner())
        print("Player " + winner_string + " won the game!")

    def update_game(self, game: Game):
        self._game_obj = game
        self._size = self._game_obj.board.size
