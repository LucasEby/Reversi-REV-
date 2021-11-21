import string
import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class EndGamePageView(BasePageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        game_obj: Game,
        rematch_cb: Callable[[Game], None],
        play_again_cb: Callable[[Game], None],
        window,
    ) -> None:
        """
        :param game_obj: A specific game object who's attributes will be accessed and displayed.
        :param rematch_cb: Callback function for playing the same game mode against the same opponent
        :param play_again_cb: Callback function for playing the same mode again
        :param play_different_mode_cb: Callback function for changing the game mode

        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        self._game_obj: Game = game_obj
        self._go_home_callback = go_home_cb
        self._rematch_callback = rematch_cb
        self._play_again_callback = play_again_cb
        super().__init__(window=window)

    def __display(self) -> None:
        """
        Packs the End Game frame and its 5 elements
        """
        self.__score_label().pack()
        self.__winner_label().pack()
        self.__play_again_button().pack()
        self.__rematch_button().pack()
        self._frame.lift()

    def __rematch_button(self) -> tk.Button:
        """
        Builds the rematch button
        :return: Button labled rematch
        """
        return tk.Button(
            self._frame,
            text="Rematch",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._rematch_callback,
        )

    def __play_again_button(self) -> tk.Button:
        """
        Builds the play again button
        :return: Button labled Play Again
        """
        return tk.Button(
            self._frame,
            text="Play Again",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._play_again_callback,
        )

    def __score_label(self) -> tk.Label:
        """
        returns the label stating the game's score.
        :return: label "Score"
        """
        return tk.Label(self._frame, text = ("Score: " + str(self._game_obj.get_score())))

    def __winner_label(self) -> tk.Label:
        """
        returns the label containing winner of the game.
        :return: lable "Winner"
        """
        return tk.Label(self._frame, text = ("Winner: " + str(self._game_obj.get_winner())))
"""
windows = tk.tk()
thing = EndGamePageView(None, None, None, None, windows)
windows.mainloop()
"""
