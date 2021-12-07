import tkinter as tk
from typing import List, Callable, Tuple

from client.model.cell import Cell, CellState
from client.model.game import Game
from client.views.base_page_view import BasePageView


class CreateAccountPageView(BasePageView):
    def __init__(
        self, go_home_cb: Callable[[], None], login_cb: Callable[[str, str], None]
    ) -> None:
        """
        View to create a new account
        :param go_home_callback: Callback to call when user requested going to the home screen
        :param login_callback: Callback to handle creating a new account
        """
        super().__init__(go_home_callback=go_home_cb)
        self._go_home_callback = go_home_cb
        self._login_callback = login_cb
        self._username_entry = ""
        self._password_entry = ""

        self._title_label: tk.Label = self.__title_label()
        self._username_field: tk.Entry = self.__username_field()
        self._password_field: tk.Entry = self.__password_field()
        self._submit_button: tk.Button = self.__submit_button()

        self.display()

    def display(self) -> None:
        """
        Draws the Create Account window and its elements
        """
        super().display()
        self._title_label.pack()
        self._username_field.pack()
        self._password_field.pack()
        self._submit_button.pack()

    def destroy(self) -> None:
        """
        Destroy everything in the Create Account Page
        """
        super().destroy()
        self._title_label.destroy()
        self._username_field.destroy()
        self._password_field.destroy()
        self._submit_button.destroy()

    def __title_label(self) -> tk.Label:
        """
        Displays the page's title, "Create an Account"
        :returns: tkinter label
        """
        return tk.Label(self._frame, text="Create an Account")

    def __username_field(self) -> tk.Entry:
        """
        Creates the entry field for the username being attempted
        :returns: tkinter entry
        """
        return tk.Entry(self._frame, textvariable=self._username_entry)

    def __password_field(self) -> tk.Entry:
        """
        Creates the entry field for the password being attempted

        :returns: tkinter entry
        """
        return tk.Entry(self._frame, textvariable=self._password_entry)

    def __submit_button(self) -> tk.Button:
        """
        Creates the button for the password being attempted
        :returns: tkinter button
        """
        return tk.Button(
            self._frame,
            text="Submit",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command=lambda: self._login_callback(
                self._username_entry, self._password_entry
            ),
        )
