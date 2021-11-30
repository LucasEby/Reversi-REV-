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
        self._frame.pack()
        self.__game_obj: Game = game_obj
        self.__size: int = game_obj.board.size
        self.__place_tile_cb = place_tile_cb
        self.__forfeit_cb = forfeit_cb
        self.__preferences = preferences
        self.__end_game_callback = end_game_callback
        self.__window = window

        self.__btn_size: int = int(45 / (self.__size + 1))
        self.__btn_forfeit = tk.Button(
            self._frame,
            text="forfeit",
            height=self.__btn_size,
            width=self.__btn_size,
            fg="black",
            bg="purple",
            command=self.__forfeit_cb,
        )

    def run(self):
        self.display()

    def display(self):
        self.__display_board()
        self.__display_score()
        self.__btn_forfeit.grid(column=0, row=self.__size)
        self._frame.lift()
        self._frame.mainloop()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        board_state: List[List[CellState]] = self.__game_obj.board.get_state()
        # player_num = self.__game_obj.curr_player
        valid_moves: List[List[bool]] = self.__game_obj.get_valid_moves()  #row, col
        # plyr_num: int, posn: Tuple[int, int], brd: Board) -> bool:
        player1_color: string = str(self.__preferences.get_my_disk_color()).lower()
        player2_color: string = str(self.__preferences.get_opp_disk_color()).lower()
        # line_color = self.__preferences.get_line_color() # not supported with grid()
        game_color: string = str(self.__preferences.get_board_color()).lower()

        for row in range(0, self.__size):
            for col in range(0, self.__size):
                if board_state[row][col] == CellState.player1:
                    tk.Button(self._frame, text="Player 1", fg=player1_color, bg=player1_color, height=self.__btn_size,
                              width=self.__btn_size, state=tk.DISABLED).grid(column=col, row=row)
                elif board_state[row][col] == CellState.player2:
                    tk.Button(self._frame, text="Player 2", fg=player2_color, bg=player2_color, height=self.__btn_size,
                              width=self.__btn_size, state=tk.DISABLED).grid(column=col, row=row)
                elif (board_state[row][col] == CellState.empty) and valid_moves[row][col]:
                   tk.Button(
                       self._frame,
                       bg="green",
                       fg=game_color,
                       height=self.__btn_size,
                       width=self.__btn_size,
                       state=tk.NORMAL,
                       command=self.__handle_place_tile_cb,
                   ).grid(column=col, row=row) # (tuple[row: int, col: int]),
                else:
                    # board_state[row][col].state == CellState.empty:
                    tk.Button(
                        self._frame,
                        bg="green",
                        fg=game_color,
                        height=self.__btn_size,
                        width=self.__btn_size,
                        state=tk.DISABLED,
                    ).grid(column=col, row=row)

    def __handle_place_tile_cb(self):
        print("fish")

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
        tk.Label(self._frame, fg="orange", text=player1_string).grid(column=self.__size, row=self.__size)
        tk.Label(self._frame, fg="purple", text=player2_string).grid(column=self.__size, row=(self.__size + 1))

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
