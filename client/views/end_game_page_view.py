import tkinter as tk
from typing import Callable
from client.model.game import Game
from client.views.home_button_page_view import HomeButtonPageView


class EndGamePageView(HomeButtonPageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        play_again_cb: Callable[[], None],
        play_different_mode_cb: Callable[[], None],
        game: Game,
    ) -> None:
        """
        View to choose what to do after the game ends

        :param go_home_cb: Callback to call when user requested going to the home screen
        :param play_again_cb: Callback function for when play again button is pressed
        :param play_different_mode_cb: Callback function for when play different mode button is pressed
        :param game: A specific game object whose attributes will be accessed and displayed.
        """
        super().__init__(go_home_callback=go_home_cb)
        self._play_again_callback: Callable[[], None] = play_again_cb
        self._play_different_mode_callback: Callable[[], None] = play_different_mode_cb
        self._game: Game = game

        self._score_label: tk.Label = self.__score_label()
        self._winner_label: tk.Label = self.__winner_label()
        self._play_again_button: tk.Button = self.__play_again_button()
        self._play_different_mode_button: tk.Button = (
            self.__play_different_mode_button()
        )
        self.display()

    def display(self) -> None:
        """
        Draws the End Game windows and its elements
        """
        super().display()
        self._score_label.pack()
        self._winner_label.pack()
        self._play_again_button.pack()
        self._play_different_mode_button.pack()

    def destroy(self) -> None:
        """
        Destroy everything on the frame
        """
        super().destroy()
        self._score_label.destroy()
        self._winner_label.destroy()
        self._play_again_button.destroy()
        self._play_different_mode_button.destroy()

    def __play_again_button(self) -> tk.Button:
        """
        Builds the play again button
        """
        return tk.Button(
            self._frame,
            text="Play Again",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command=self._play_again_callback,
        )

    def __play_different_mode_button(self) -> tk.Button:
        """
        Builds the play different mode button
        """
        return tk.Button(
            self._frame,
            text="Play Different Mode",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command=self._play_different_mode_callback,
        )

    def __score_label(self) -> tk.Label:
        """
        Creates label to display the game's score.
        """
        return tk.Label(
            self._frame,
            text=f"Score: {self._game.get_score()[0]} - {self._game.get_score()[1]}",
        )

    def __winner_label(self) -> tk.Label:
        """
        Creates label to display the game's winner.
        """
        return tk.Label(self._frame, text=f"Winner: Player {self._game.get_winner()}")
