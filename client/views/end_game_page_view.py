import string
import tkinter as tk
from typing import Callable
from client.model.game import Game
from client.views.home_button_page_view import HomeButtonPageView


class EndGamePageView(HomeButtonPageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        game: Game,
        play_again_cb: Callable[[Game], None],
        play_different_mode_cb: Callable[[], None],
        go_home_callback,
        window,
    ) -> None:
        """
        :param game: A specific game object who's attributes will be accessed and displayed.
        :param play_again_cb: Callback function for playing the same mode again
        :param play_different_mode_cb: Callback function for changing the game mode

        :param go_home_cb: Callback to call when user requested going to the home screen
        """
        super().__init__(go_home_callback=go_home_callback, window=window)
        self._game: Game = game
        self._go_home_callback = go_home_cb
        self._play_again_callback = play_again_cb
        self._play_different_mode_callback = play_different_mode_cb
        self.__padx = 22
        self.__btn_size = 22
        self.__btn_home: tk.Button = self.add_home_button(padx=self.__padx, btn_size=self.__btn_size)

    def display(self) -> None:
        """
        draws the End Game windows and its 5 elements
        """
        self.__score_label().pack()
        self.__winner_label().pack()
        self.__play_again_button().pack()
        self.__play_different_mode_button().pack()
        self.__btn_home.pack()
        self._frame.lift()  # self._frame.place()
        # Start window main loop:
        self._frame.mainloop()

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
            command=self.__handle_play_again_callback,
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
            command=self.__handle_play_different_mode,
        )

    def __handle_play_again_callback(self):
        self._play_again_callback(self._game)
        self._exit()
        # self._frame.destroy()

    def __handle_play_different_mode(self):
        self._play_different_mode_callback()
        self._exit()
        # self._frame.destroy()

    def __score_label(self) -> tk.Label:
        """
        Prints out the game's score.
        """
        # return tk.Label(str(self._game_obj.get_score()))
        return tk.Label(self._frame, text=("Score: " + str(self._game.get_score())))

    def __winner_label(self) -> tk.Label:
        """
        Prints out the winner of the game.
        """
        # return tk.Label(str(self._game_obj.get_score()))
        return tk.Label(self._frame, text=("Winner: " + str(self._game.get_winner())))

    def display_winner(self) -> None:
        """
        Prints out the winner of the game.
        """
        winner: string = str(self._game.get_winner())
        winner_message = "Player " + winner + " won the game!"
        self.__destroy_buttons_and_load(winner_message)
        self._exit()
        # self._frame.destroy()
        # tk.Label(self._frame, fg="white", title=winner_message).pack()

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

# def __rematch_button(self) -> tk.Button:
#     """
#     Builds the rematch button
#     """
#     return tk.Button(
#         self._frame,
#         text="Rematch",
#         width=25,
#         height=5,
#         bg="blue",
#         fg="yellow",
#         command=self.__handle_rematch_callback,
#     )

# def __handle_rematch_callback(self):
#     self._rematch_callback(self._game)
#     self._exit()
#     self._frame.destroy()
"""
windows = tk.tk()
thing = EndGamePageView(None, None, None, None, windows)
windows.mainloop()
"""
