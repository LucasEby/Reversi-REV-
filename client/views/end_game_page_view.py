import string
import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class EndGamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(
        self,
        game_obj: Game,
        rematch_cb: Callable[[int], None],
        play_again_cb: Callable[[int], None],
        play_different_mode_cb: Callable[[int], None],
    ) -> None:
        """

        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param rematch_cb: Callback function for playing the same game mode against the same opponent
        :param play_again_cb: Callback function for playing the same mode again
        :param play_different_mode_cb: Callback function for changing the game mode
        """
        self._game_obj: Game = game_obj
        self._rematch_callback = rematch_cb
        self._play_again_callback = play_again_cb
        self._play_different_mode_callback = play_different_mode_cb
        super().__init__()

    def display(self) -> None:
        """
        draws the End Game windows and its 5 elements
        """
        window = tk.Tk()
        self.__score_label().pack()
        self.__winner_label().pack()
        self.__play_again_button().pack()
        self.__rematch_button().pack()
        self.__play_different_mode_button().pack()

        window.mainloop()

    def __rematch_button(self) -> tk.Button:
        """
        Builds the rematch button
        """
        return tk.Button(
            text="Rematch",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._rematch_callback,
        )

    def __play_again_button(self) -> tk.Button:
        """
        Builds the play again button
        """
        return tk.Button(
            text="Play Again",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._play_again_callback,
        )

    def __play_different_mode_button(self) -> tk.Button:
        """
        Builds the play different mode button
        """
        return tk.Button(
            text="Play Diiffernt Mode",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._play_different_mode_callback,
        )

    def __score_label(self) -> tk.Label:
        """
        Prints out the game's score.
        """
        return tk.Label(str(self._game_obj.get_score()))

    def __winner_label(self) -> tk.Label:
        """
        Prints out the winner of the game.
        """
        return tk.Label(str(self._game_obj.get_score()))
