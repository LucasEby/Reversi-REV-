import string
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.model.preference import Preference
from client.views.base_page_view import BasePageView
import tkinter as tk


def do_place_tile(__handle_place_tile_cb, r, c):
    __handle_place_tile_cb(r, c)


class PlayGamePageView(BasePageView):
    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game: Game,
        place_tile_cb: Callable[[Tuple[int, int]], None],
        forfeit_cb: Callable[[int], None],
        preferences: Preference,
        end_game_callback,
        window,
    ) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board
        :param game: A specific game object who's attributes will be accessed and displayed.
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        super().__init__(window=window)
        self._frame.pack()
        self.__game: Game = game
        self.__size: int = game.board.size
        self.__place_tile_cb = place_tile_cb
        self.__forfeit_cb = forfeit_cb
        self.__preferences = preferences
        self.__end_game_callback = end_game_callback
        self.__window = window
        self.__player1_color: string = str(
            self.__preferences.get_my_disk_color()
        ).lower()
        self.__player2_color: string = str(
            self.__preferences.get_opp_disk_color()
        ).lower()
        self.__game_bg = self.__preferences.get_line_color()
        self.__padx = self.__pady = 22
        self.__game_color: string = str(self.__preferences.get_board_color()).lower()
        self.__btn_size: int = int(45 / (self.__size + 2 + self.__padx))
        self.__btn_forfeit = tk.Button(
            self._frame,
            text="forfeit",
            padx=self.__padx,
            pady=self.__pady,
            height=self.__btn_size,
            width=self.__btn_size,
            fg="black",
            bg="purple",
            command=self.__handle_forfeit,
        )

    def run(self):
        self.display()

    def display(self):
        self.__display_board()
        self.__display_score()
        self.__display_current_player()
        self.__btn_forfeit.grid(column=0, row=self.__size)
        self._frame.lift()
        # self._frame.place()
        self._frame.mainloop()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        board_state: List[List[CellState]] = self.__game.board.get_state()
        valid_moves: List[List[bool]] = self.__game.get_valid_moves()  # row, col

        for row in range(0, self.__size):
            for col in range(0, self.__size):
                if board_state[row][col] == CellState.player1:
                    tk.Button(
                        self._frame,
                        text="Player 1",
                        padx=self.__padx,
                        pady=self.__pady,
                        fg=self.__player1_color,
                        bg=self.__player1_color,
                        height=self.__btn_size,
                        width=self.__btn_size,
                        state=tk.DISABLED,
                    ).grid(column=col, row=row)
                elif board_state[row][col] == CellState.player2:
                    tk.Button(
                        self._frame,
                        text="Player 2",
                        padx=self.__padx,
                        pady=self.__pady,
                        fg=self.__player2_color,
                        bg=self.__player2_color,
                        height=self.__btn_size,
                        width=self.__btn_size,
                        state=tk.DISABLED,
                    ).grid(column=col, row=row)
                elif (board_state[row][col] == CellState.empty) and not valid_moves[
                    row
                ][col]:
                    tk.Button(
                        self._frame,
                        padx=self.__padx,
                        pady=self.__pady,
                        bg="green",
                        fg=self.__game_color,
                        height=self.__btn_size,
                        width=self.__btn_size,
                        state=tk.DISABLED,
                    ).grid(column=col, row=row)
                else:
                    ButtonMaker(
                        frame=self._frame,
                        padx=self.__padx,
                        pady=self.__pady,
                        row=row,
                        col=col,
                        bg="green",
                        fg="green",
                        btn_size=self.__btn_size,
                        handle_place_tile_callback=self.__handle_place_tile_cb,
                    )

    def __handle_place_tile_cb(self, row: int, col: int):
        temp_tuple: tuple[int, int] = (row, col)
        self.__place_tile_cb(temp_tuple)

    def __display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple: tuple = self.__game.get_score()
        player1_string: string = "Player 1's score: " + str(temp_tuple[0])
        player2_string: string = "Player 2's score: " + str(temp_tuple[1])
        tk.Label(self._frame, fg="orange", text=player1_string).grid(
            column=self.__size, row=self.__size
        )
        tk.Label(self._frame, fg="purple", text=player2_string).grid(
            column=self.__size, row=(self.__size + 1)
        )

    def __display_current_player(self) -> None:
        """
        Displays the player whose move it currently is.
        """
        current_player: int = self.__game.curr_player
        turn_string: string = "Player turn: Player" + str(current_player)
        tk.Label(self._frame, fg="red", text=turn_string).grid(
            column=self.__size, row=(self.__size + 2)
        )

    def update_game(self, game: Game):
        self.__game = game
        self.__size = self.__game.board.size

    def __handle_forfeit(self):
        self.__forfeit_cb(self.__game.curr_player)
        self._exit()
        self._frame.destroy()

    def execute_end_game(self):
        # self.__destroy_buttons_and_load("The game has ended!")
        # self._exit()
        self.__end_game_callback()
        self._exit()
        self._frame.destroy()

    def display_player_forfeit(self, player_num):
        if player_num == 1:
            forfeit_message = (
                "Player " + str(player_num) + " forfeited the game! Player 2 wins!"
            )
        else:
            forfeit_message = (
                "Player " + str(player_num) + " forfeited the game! Player 1 wins!"
            )
        self.__destroy_buttons_and_load(forfeit_message)
        self._exit()
        self._frame.destroy()

    def __destroy_buttons_and_load(self, load_message) -> None:
        """
        Destroys the buttons and displays the loading screen.

        :param self: the PickGamePageView object.
        :param load_message: the load message that is displayed to the user
        :return: None
        """
        for widgets in self._frame.winfo_children():
            widgets.destroy()
        L = tk.Label(self._frame, text=load_message)
        L.pack()
        # self._exit()


class ButtonMaker:
    def __init__(
        self, frame, padx, pady, row, col, bg, fg, btn_size, handle_place_tile_callback
    ) -> None:
        self.frame: tk.Frame = frame
        self.row = row
        self.col = col
        self.bg = bg
        self.fg = fg
        self.btn_size = btn_size
        self.state = tk.NORMAL
        self.__handle_place_tile_cb = handle_place_tile_callback
        self.button = tk.Button(
            self.frame,
            padx=padx,
            pady=pady,
            bg=self.bg,
            fg=self.fg,
            height=self.btn_size,
            width=self.btn_size,
            state=tk.NORMAL,
            command=lambda: do_place_tile(
                self.__handle_place_tile_cb, r=self.row, c=self.col
            ),
        ).grid(row=row, column=col)


# self.__fg = [[]]
#         temp_fg = []
#         self.__bg = [[]]
#         temp_bg = []
#         self.__button_list = [[]]
#         temp_button_list = []
#         self.__row_list = []
#         self.__col_list = []
#         for row in range(0, self.__size):
#             self.__row_list.append(row)
#             self.__col_list.append(row)
#             for col in range(0, self.__size):
#                 temp_fg.append("")
#                 temp_bg.append("")
#             self.__fg.append(temp_fg)
#             self.__bg.append(temp_bg)
#
#         for row in range(0, self.__size):
#             for col in range(0, self.__size):
#                 a = ButtonMaker(frame=self._frame,
#                     row=row,
#                     col=col,
#                     bg="green",
#                     fg="green",
#                     btn_size=self.__btn_size,
#                     handle_place_tile_callback=self.__handle_place_tile_cb)
#                 temp_button_list.append(a)
#             self.__button_list.append(temp_button_list)


# temp_button_list.append(tk.Button(
#                     self._frame,
#                     bg=self.__bg[row][col],
#                     fg=self.__fg[row][col],
#                     height=self.__btn_size,
#                     width=self.__btn_size,
#                     state=tk.NORMAL,
#                     command=lambda: doSomething(self.__handle_place_tile_cb, r=tk.Button.grid_location(self.__row[row], self.),
#                                                 c=self.__grid_location[row][col].get_col()),
#                 ))

# print("initialized row: " + str(row))
# print("initialized col: " + str(col))
# a = tk.Button(
#     self._frame,
#     bg="green",
#     fg="green",
#     width=self.__btn_size,
#     height=self.__btn_size,
#     command=lambda: doSomething(self.__handle_place_tile_cb, r=row, c=col)
# ).grid(row=row, column=col)

# (board_state[row][col] == CellState.empty) and valid_moves[row][col]:
#                     self.__button_list[row][col].plot_button(row=row, col=col)  # grid(column=col, row=row)
#                     self.__button_list[row][col].button.grid(column=self.__button_list[row][col].col, row=self.__button_list[row][col].row)
#                 (tuple[row: int, col: int]),
#                 else:
#                     # board_state[row][col].state == CellState.empty:
#                     tk.Button(
#                         self._frame,
#                         bg="green",
#                         fg=game_color,
#                         height=self.__btn_size,
#                         width=self.__btn_size,
#                         state=tk.DISABLED,
#                     ).grid(column=col, row=row)
