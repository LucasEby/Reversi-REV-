import tkinter as tk
from typing import Callable

from client.views.home_button_page_view import HomeButtonPageView


class CreateAccountPageView(HomeButtonPageView):
    def __init__(
        self,
        go_home_cb: Callable[[], None],
        login_cb: Callable[[str, str], None],
    ) -> None:
        """
        View to create a new account
        :param go_home_cb: Callback to call when user requested going to the home screen
        :param login_cb: Callback to handle creating a new account
        """
        super().__init__(go_home_callback=go_home_cb)
        self._go_home_callback = go_home_cb
        self._login_callback = login_cb
        self._username_entry = tk.StringVar()
        self._password_entry = tk.StringVar()

        self._title_label: tk.Label = self.__title_label()
        self._username_label: tk.Label = self.__label("Username: ")
        self._username_field: tk.Entry = self.__username_field()
        self._password_label: tk.Label = self.__label("Password: ")
        self._password_field: tk.Entry = self.__password_field()
        self._submit_button: tk.Button = self.__submit_button()

        self.display()

    def display(self) -> None:
        """
        Draws the Create Account window and its elements
        """
        super().display()
        self._title_label.pack()
        self._username_label.pack()
        self._username_field.pack()
        self._password_label.pack()
        self._password_field.pack()
        self._submit_button.pack(pady=5)

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
            padx=10,
            pady=5,
            bg="green",
            fg="white",
            command=lambda: self._login_callback(
                self._username_entry.get(), self._password_entry.get()
            ),
        )

    def __label(self, message: str) -> tk.Label:
        """
        Creates label to display the game's score.
        """
        return tk.Label(self._frame, text=message)
