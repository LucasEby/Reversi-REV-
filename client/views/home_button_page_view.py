from typing import Callable

from client.views.base_page_view import BasePageView
import tkinter as tk


class HomeButtonPageView(BasePageView):

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        window,
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.
        """
        super().__init__(window=window)
        self._frame.pack()
        self._window = window
        self._home_button_callback: Callable[[], None] = go_home_callback

    def _handle_home_button_callback(self):
        self.__execute_home_button_callback()
        self._exit()

    def __execute_home_button_callback(self):
        self._home_button_callback()

    def display(self) -> None:
        """
        Displays home button to user
        TODO: Implement this with GUI
        """
        pass

    def add_home_button(self, padx=10, btn_size=10) -> tk.Button:
        """
        Builds the home button
        """
        return tk.Button(
            self._frame,
            text="Go Home",
            padx=padx,
            pady=padx,
            width=btn_size,
            height=btn_size,
            fg="black",
            bg="purple",
            command=self._handle_home_button_callback,
        )
