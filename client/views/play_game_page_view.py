import string
from typing import List, Callable, Tuple, Optional

from client.model.cell import CellState
from client.model.game import Game
from client.model.game_manager import GameManager
from client.model.preference import Preference
from client.model.user import User
from client.views.base_page_view import BasePageView
import tkinter as tk


class PlayGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game_manager: GameManager,
        preferences: Preference,
        place_tile_cb: Callable[[Tuple[int, int]], None],
        forfeit_cb: Callable[[], None],
    ) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board

        :param game: A specific game object who's attributes will be accessed and displayed.
        :param preferences: Main user preferences
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        super().__init__()
        self._game_manager: GameManager = game_manager
        self._game: Game = self._game_manager.game
        self._size: int = self._game.board.size
        self._place_tile_cb: Callable[[Tuple[int, int]], None] = place_tile_cb
        self._forfeit_cb: Callable[[], None] = forfeit_cb
        self._preferences: Preference = preferences
        self._player1_color: str = self._preferences.get_my_disk_color().lower()
        self._player2_color: str = self._preferences.get_opp_disk_color().lower()
        self._game_bg: str = self._preferences.get_line_color().lower()
        self._padx: int = 1
        self._pady: int = self._padx
        self._button_height: int = int(3.0 / 8 * self._size)
        self._button_width: int = self._size
        self._game_color: str = self._preferences.get_board_color().lower()
        self._btn_forfeit: tk.Button = tk.Button(
            self._frame,
            text="Forfeit",
            height=self._button_height,
            width=self._button_width,
            fg="black",
            bg="purple",
            command=self._forfeit_cb,
        )
        self._board_buttons: List[List[tk.Button]] = [
            [
                tk.Button(
                    self._frame,
                    padx=self._padx,
                    pady=self._pady,
                    fg=self._player1_color,
                    bg=self._player1_color,
                    height=self._button_height,
                    width=self._button_width,
                    command=lambda row=row, col=col: self._place_tile_cb(  # type: ignore
                        (row, col)
                    ),
                )
                for col in range(self._size)
            ]
            for row in range(self._size)
        ]
        self.display()

    def display(self) -> None:
        """
        Displays all components of the page
        """
        super().display()
        self.__display_board()
        self.__display_score()
        self.__display_forfeit()
        self.__display_current_player()

    def destroy(self) -> None:
        """
        Destroys all components of the page
        """
        super().destroy()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        board_state: List[List[CellState]] = self._game.board.get_state()
        valid_moves: List[List[bool]] = self._game.get_valid_moves()  # row, col

        for row in range(0, self._size):
            for col in range(0, self._size):
                if board_state[row][col] == CellState.player1:
                    self._board_buttons[row][col].configure(
                        text="Player 1",
                        fg=self._player1_color,
                        bg=self._player1_color,
                        state=tk.DISABLED,
                    )
                elif board_state[row][col] == CellState.player2:
                    self._board_buttons[row][col].configure(
                        text="Player 2",
                        fg=self._player2_color,
                        bg=self._player2_color,
                        state=tk.DISABLED,
                    )
                elif (board_state[row][col] == CellState.empty) and not valid_moves[
                    row
                ][col]:
                    self._board_buttons[row][col].configure(
                        bg="green",
                        fg=self._game_color,
                        state=tk.DISABLED,
                    )
                else:
                    self._board_buttons[row][col].configure(
                        bg="light green",
                        fg="light green",
                        state=tk.NORMAL,
                    )
                self._board_buttons[row][col].grid(
                    row=row, column=col, padx=self._padx, pady=self._pady
                )

    def __display_forfeit(self) -> None:
        """
        Displays forfeit button
        """
        self._btn_forfeit.grid(column=0, row=self._size)

    def __display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple: Tuple[int, int] = self._game.get_score()
        p1_str: str
        p2_str: str
        p1_user: Optional[User] = self._game_manager.get_player1().get_user()
        p2_user: Optional[User] = self._game_manager.get_player2().get_user()
        if p1_user is not None:
            p1_str = f"{p1_user.get_username()}'s score: {temp_tuple[0]}"
        else:
            p1_str = f"Player 1's score: {temp_tuple[0]}"
        if p2_user is not None:
            p2_str = f"{p2_user.get_username()}'s score: {temp_tuple[1]}"
        else:
            p2_str = f"Player 2's score: {temp_tuple[1]}"
        tk.Label(self._frame, fg="orange", text=p1_str).grid(
            column=self._size, row=self._size + 1
        )
        tk.Label(self._frame, fg="purple", text=p2_str).grid(
            column=self._size, row=self._size + 2
        )

    def __display_current_player(self) -> None:
        """
        Displays the player whose move it currently is.
        """
        current_player: int = self._game.curr_player
        turn_string: str = f"Player {current_player}'s turn"
        tk.Label(self._frame, fg="red", text=turn_string).grid(
            column=self._size, row=self._size + 3
        )

    def update_game(self, game: Game):
        self._game = game
        self._size = self._game.board.size
