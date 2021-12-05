import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class CreateAccountPageView(BasePageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        frame,
    ) -> None:
        """
        TODO add proper comment here
        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        self._go_home_callback = go_home_cb

        self._frame = frame

        super().__init__(window=frame)

    def __display(self) -> None:
        """
        Packs/Grids the End Game frame and its 5 elements
        """
        # TODO: ADD IN THE DISPLAY
        self._frame.pack()
        self._frame.lift()

    def __title_label(self) -> tk.Label:
        """
        Prints out the games's name
        """
        return tk.Label(self._frame, text="Create an Account")

    def __username_field(self) -> tk.Entry:
        """
        Creates the entry field for the username being attempted

        :returns: tkinter entry object
        """
        return tk.Entry(self._topframe, textvariable=self._username_entry)

    def __password_field(self) -> tk.Entry:
        """
        Creates the entry field for the apssword being attempted

        :returns: tkinter entry object
        """
        return tk.Entry(self._topframe, textvariable=self._password_entry)

    def __default_preferences(self) -> tk.Entry:
        # TODO what are the preferences
        pass

    def __submit_button(self) -> tk.Button:
        """
        Builds the rematch button
        TODO: NEED TO PASS THE USERNAME AND PASSWORD TO THE SERVER HERE
        """
        return tk.Button(
            self._topframe,
            text="Submit",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            # command = ?????,
        )
