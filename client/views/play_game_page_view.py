import string
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.model.preference import Preference
from client.views.base_page_view import BasePageView
import tkinter as tk


class PlayGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game_obj: Game,
        place_tile_cb: Callable[[Tuple[int, int]], None],
        forfeit_cb: Callable[[int], None],
        preferences: Preference,
        end_game_callback,
        window,
    ) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board
        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        super().__init__(window=window)
        self.__game_obj: Game = game_obj
        self.__size: int = game_obj.board.size
        self.__place_tile_cb = place_tile_cb
        self.__forfeit_cb = forfeit_cb
        self.__preferences = preferences
        self.__end_game_callback = end_game_callback
        self.__window = window
        # self.play_game_frame = tk.Frame(self.window, padding=10)
        self._frame.grid()
        self.__btn_forfeit = tk.Button(
            self._frame,
            text="forfeit",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self.__forfeit_cb,
        )

    def display(self):
        self.__display_board()
        self._frame.lift()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        board_state: List[List[Cell]] = self.__game_obj.board.get_state()
        player1_color = self.__preferences.get_my_disk_color()
        player2_color = self.__preferences.get_opp_disk_color()
        # line_color = self.__preferences.get_line_color() # not supported with grid()
        game_color = self.__preferences.get_board_color()

        for row in range(0, self.__size + 1):
            for col in range(0, self.__size + 1):
                if board_state[row][col].state == CellState.player1:
                    tk.Label(self._frame, fg=player1_color).grid(column=col, row=row)
                elif board_state[row][col].state == CellState.player2:
                    tk.Label(self._frame, fg=player2_color).grid(column=col, row=row)
                elif board_state[row][col].state == CellState.empty:
                    tk.Button(
                        self._frame,
                        fg=game_color,
                        command=self.__place_tile_cb((row, col)),
                    ).grid(column=col, row=row)

    def __destroy_buttons_and_load(self, load_message) -> None:
        """
        Destroys the buttons and displays the loading screen.

        :param self: the PickGamePageView object.
        :param load_message: the load message that is displayed to the user
        :return: None
        """
        self._frame.grid.destroy()
        self.__btn_forfeit.destroy()
        L = tk.Label(self._frame, text=load_message)
        L.pack()

    def __display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple: tuple = self.__game_obj.get_score()
        player1_string: string = "Player 1's score: " + str(temp_tuple[0])
        player2_string: string = "Player 2's score: " + str(temp_tuple[1])
        tk.Label(self._frame, fg="white", title=player1_string).pack()
        tk.Label(self._frame, fg="white", title=player2_string).pack()

    # TODO: move display_winner into the end game view
    def display_winner(self) -> None:
        """
        Prints out the winner of the game.
        """
        winner: string = str(self.__game_obj.get_winner())
        winner_message = "Player " + winner + " won the game!"
        self.__destroy_buttons_and_load(winner_message)
        # tk.Label(self._frame, fg="white", title=winner_message).pack()

    def update_game(self, game: Game):
        self.__game_obj = game
        self.__size = self.__game_obj.board.size

    def display_player_forfeit(self, player_num):
        if player_num == 1:
            forfeit_message = (
                "Player " + player_num + " forfeited the game! Player 2 wins!"
            )
        else:
            forfeit_message = (
                "Player " + player_num + " forfeited the game! Player 1 wins!"
            )


# def __tile_clicked(self, row: int, col: int) -> None:
#
#     print("fish")
#     # def __display_tile_placement(self) -> None:
#     #     """
#     #     Displays graphic for user to enter tile placement info
#     #     """
#     #     valid_input: bool = False
#     #     row: int = 0
#     #     col: int = 0
#     #     print(f"\nPlayer {self._game_obj.curr_player}'s turn")
#     #     while not valid_input:
#     #         row_str: str = input("Enter row for disk: ")
#     #         col_str = input("Enter col for disk: ")
#     #         try:
#     #             row = int(row_str) - 1
#     #             col = ord(col_str.lower()) - 97
#     #         except ValueError:
#     #             print("Invalid row or col. Please try again.")
#     #             continue
#     #         valid_input = True
#     #     self._place_tile_cb((row, col))
