from typing import Callable

from client.tkinter_gui import TkinterGUI
from client.views.base_page_view import BasePageView
import tkinter as tk


class HomeButtonPageView(BasePageView):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.
        """
        super().__init__()
        self._home_button_callback: Callable[[], None] = go_home_callback
        self._home_button_frame: tk.Frame = tk.Frame(TkinterGUI().get_window())
        self._home_button: tk.Button = self._add_home_button()

    def _handle_home_button_callback(self):
        self.__execute_home_button_callback()

    def __execute_home_button_callback(self):
        self.destroy()
        self._home_button_callback()

    def display(self) -> None:
        """
        Displays home button to user
        """
        self._home_button.pack()
        self._home_button_frame.pack()

    def _add_home_button(self, padx=10) -> tk.Button:
        """
        Builds the home button
        """
        return tk.Button(
            self._home_button_frame,
            text="Go Home",
            padx=padx,
            pady=padx,
            fg="white",
            bg="green",
            command=self._handle_home_button_callback,
        )

    def destroy(self) -> None:
        """
        Destroys any frames in here
        """
        super().destroy()
        self._home_button_frame.destroy()
