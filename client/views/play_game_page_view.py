import string
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class PlayGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game_obj: Game,
        place_tile_cb: Callable[[Tuple[int, int]], None],
        forfeit_cb: Callable[[int], None],
    ) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board
        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param place_tile_cb: Callback function to call when a tile is placed
        :param forfeit_cb: Callback function to call when a player forfeits
        """
        self._game_obj: Game = game_obj
        self._size: int = game_obj.board.size
        self._place_tile_cb = place_tile_cb
        self._forfeit_cb = forfeit_cb
        super().__init__()

    def display(self) -> None:
        self.__display_board()
        self.__display_score()
        self.__display_tile_placement()

    def __display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        board: string = ""  # reset board string.
        board_state: List[List[CellState]] = self._game_obj.board.get_state()
        for row in range(0, self._size + 1):
            for col in range(0, self._size + 1):
                if row == 0:
                    if col > 0:
                        board = board + "   " + self.__ABC_ARRAY[col - 1]
                else:  # row > 0
                    if col == 0:
                        board += str(row)
                    else:
                        if board_state[row - 1][col - 1] == CellState.player1:
                            board += "  P1"
                        elif board_state[row - 1][col - 1] == CellState.player2:
                            board += "  P2"
                        elif board_state[row - 1][col - 1] == CellState.empty:
                            board += "  __"
                if col == self._size:
                    board += "\n"
        print(board)

    def __display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple: tuple = self._game_obj.get_score()
        temp_string0: string = str(temp_tuple[0])
        temp_string1: string = str(temp_tuple[1])
        print("Player 1's score: " + temp_string0)
        print("Player 2's score: " + temp_string1)

    def __display_tile_placement(self) -> None:
        """
        Displays graphic for user to enter tile placement info
        """
        valid_input: bool = False
        row: int = 0
        col: int = 0
        print(f"\nPlayer {self._game_obj.curr_player}'s turn")
        while not valid_input:
            row_str: str = input("Enter row for disk: ")
            col_str = input("Enter col for disk: ")
            try:
                row = int(row_str) - 1
                col = ord(col_str.lower()) - 97
            except ValueError:
                print("Invalid row or col. Please try again.")
                continue
            valid_input = True
        self._place_tile_cb((row, col))

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
