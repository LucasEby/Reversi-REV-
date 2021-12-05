import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class PreferencesPageView(BasePageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        # TODO: add callbacks
        frame,
    ) -> None:
        """
        TODO add proper comment here
        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        self._go_home_callback = go_home_cb
        # TODO: add callbacks

        self._frame = frame
        # self._topframe = tk.Frame(self._frame)

        self._board_size_entry = ""
        self._password_entry = ""

        super().__init__(window=frame)

    def __display(self) -> None:
        """
        Packs/Grids the End Game frame and its 5 elements
        """
        pass
        # TODO: ADD IN THE DISPLAY FOR THE TOP ELOS

        # self._frame.lift()

    def __title_label(self) -> tk.Label:
        """
        Prints out the games's name
        """
        return tk.Label(self._frame, text="Manage Preferences")

    def __board_Size_field(self) -> tk.Entry:
        """
        Creates the entry field for the username being attempted

        :returns: tkinter entry object
        """
        return tk.Entry(self._frame, textvariable=self._board_size_entry)

    def __submit_button(self) -> tk.Button:
        """
        Builds the button to submit changes to the preferences
        TODO: NEED TO PASS THE USERNAME AND PASSWORD TO THE SERVER HERE
        """
        return tk.Button(
            self._topframe,
            text="SUBMIT",
            width=25,
            height=5,
            # bg="blue",fg="yellow",
            # command=,
        )
