import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class WelcomePageView(BasePageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        login_cb: Callable[[Game], None],
        create_account_cb: Callable[[Game], None],
        guest_cb: Callable[[Game], None],
        frame,
    ) -> None:
        """
        TODO add proper comment here
        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        self._go_home_callback = go_home_cb
        self._login_callback = login_cb
        self._create_account_callback = create_account_cb
        self._play_as_guest_callback = guest_cb
        self._frame = frame
        self._username_entry = ""
        self._password_entry = ""
        super().__init__(window=frame)

    def __title_label(self) -> tk.Label:
        """
        Prints out the games's name
        """
        return tk.Label(self._frame, text="ROI-VERSI")

    def __login_username_field(self) -> tk.Entry:
        """
        Creates the entry field for the username being attempted

        :returns: tkinter entry object
        """
        return tk.Entry(self._frame, textvariable=self._username_entry)

    def __login_password_field(self) -> tk.Entry:
        """
        Creates the entry field for the apssword being attempted

        :returns: tkinter entry object
        """
        return tk.Entry(self._frame, textvariable=self._password_entry)

    def __login_button(self) -> tk.Button:
        """
        Builds the rematch button
        TODO: NEED TO PASS THE USERNAME AND PASSWORD TO THE SERVER HERE
        """
        return tk.Button(
            self._frame,
            text="Login",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._login_callback,
        )

    def __play_as_guest_button(self) -> tk.Button:
        return tk.Button(
            self._frame,
            text="Play as Guest",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._play_as_guest_callback,
        )

    def __create_account_button(self) -> tk.Button:
        return tk.Button(
            self._frame,
            text="Create a new account",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            command=self._create_account_callback,
        )
