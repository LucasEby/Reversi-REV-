import tkinter as tk
from typing import Callable, List, Tuple

from client.views.base_page_view import BasePageView


class WelcomePageView(BasePageView):
    def __init__(
        self,
        login_cb: Callable[[str, str], None],
        create_account_cb: Callable[[], None],
        guest_cb: Callable[[], None],
        elos: List[Tuple[str, int]],
    ) -> None:
        """
        Create welcome page for logging in or trying to create a new account

        :param login_cb: Callback to call when log-in button is pressed
        :param create_account_cb: Callback to call when create account button is pressed
        :param guest_cb: Callback to call when guest button is pressed
        :param elos: ELOs to display
        """
        super().__init__()
        self._login_callback: Callable[[str, str], None] = login_cb
        self._create_account_callback: Callable[[], None] = create_account_cb
        self._play_as_guest_callback: Callable[[], None] = guest_cb

        self._username_entry: tk.StringVar = tk.StringVar()
        self._password_entry: tk.StringVar = tk.StringVar()
        self._topframe: tk.Frame = tk.Frame(self._frame)
        self._title_label: tk.Label = self.__title_label()
        self._login_username_label: tk.Label = self.__login_username_label()
        self._login_password_label: tk.Label = self.__login_password_label()
        self._login_username_entry: tk.Entry = self.__login_username_field()
        self._login_password_entry: tk.Entry = self.__login_password_field()
        self._login_button: tk.Button = self.__login_button()
        self._create_account_button: tk.Button = self.__create_account_button()
        self._play_as_guest_button: tk.Button = self.__play_as_guest_button()

        self._elo_frame: tk.Frame = tk.Frame(self._frame)
        self._title_elo_label: tk.Label = self.__title_elo_label()
        self._main_elo_label: tk.Label = self.__elo_label(
            rank="Rank", username="Username", elo="ELO"
        )
        self._elo_labels: List[tk.Label] = [
            self.__elo_label(rank=str(i + 1), username=elo[0], elo=str(elo[1]))
            for i, elo in enumerate(elos)
        ]
        self.display()

    def display(self) -> None:
        """
        Packs/Grids the Welcome Page view and its elements
        """
        super().display()
        self._topframe.grid(row=0, column=0, pady=10, padx=10)
        self._title_label.grid(row=0, column=0, columnspan=3, pady=5, sticky="new")
        self._login_username_label.grid(row=1, column=0, pady=3, sticky="e")
        self._login_username_entry.grid(row=1, column=1, pady=3, sticky="w")
        self._login_password_label.grid(row=2, column=0, pady=3, sticky="e")
        self._login_password_entry.grid(row=2, column=1, pady=3, sticky="w")
        self._login_button.grid(row=1, column=2, rowspan=2, pady=3, sticky="w")
        self._create_account_button.grid(row=4, column=0, columnspan=3, pady=20)
        self._play_as_guest_button.grid(row=5, column=0, columnspan=3, pady=0)

        self._elo_frame.grid(row=1, column=0, pady=20, padx=10)
        self._title_elo_label.grid(row=0, column=0, sticky="ew")
        # self._main_elo_label.grid(row=1, column=0, sticky='w')
        for i, label in enumerate(self._elo_labels):
            label.grid(row=i + 2, column=0, sticky="w")

    def destroy(self) -> None:
        """
        Destroy all the components
        """
        super().destroy()
        self._topframe.destroy()
        self._title_label.destroy()
        self._login_username_label.destroy()
        self._login_username_entry.destroy()
        self._login_password_label.destroy()
        self._login_password_entry.destroy()
        self._login_button.destroy()
        self._create_account_button.destroy()
        self._play_as_guest_button.destroy()
        self._elo_frame.destroy()
        self._title_elo_label.destroy()
        self._main_elo_label.destroy()
        for label in self._elo_labels:
            label.destroy()

    def __title_label(self) -> tk.Label:
        """
        Create label for the title
        """
        return tk.Label(
            self._topframe, text="ROI-VERSI", font=("Arial", 50), bg="black", fg="white"
        )

    def __login_username_label(self) -> tk.Label:
        """
        Create label for username
        """
        return tk.Label(self._topframe, text="Username: ")

    def __login_password_label(self) -> tk.Label:
        """
        Create label for password
        """
        return tk.Label(self._topframe, text="Password: ")

    def __login_username_field(self) -> tk.Entry:
        """
        Creates the entry field for the username being attempted
        """
        return tk.Entry(self._topframe, textvariable=self._username_entry)

    def __login_password_field(self) -> tk.Entry:
        """
        Creates the entry field for the password being attempted
        """
        return tk.Entry(self._topframe, textvariable=self._password_entry)

    def __login_button(self) -> tk.Button:
        """
        Builds the login button
        """
        return tk.Button(
            self._topframe,
            text="Login",
            padx=30,
            pady=5,
            bg="green",
            fg="white",
            command=lambda: self._login_callback(
                self._username_entry.get(), self._password_entry.get()
            ),
        )

    def __play_as_guest_button(self) -> tk.Button:
        """
        Builds the play as guest button
        """
        return tk.Button(
            self._topframe,
            text="Play as Guest",
            padx=30,
            pady=5,
            bg="green",
            fg="white",
            command=self._play_as_guest_callback,
        )

    def __create_account_button(self) -> tk.Button:
        """
        Builds the create account button
        """
        return tk.Button(
            self._topframe,
            text="Create a new account",
            padx=30,
            pady=5,
            bg="green",
            fg="white",
            command=self._create_account_callback,
        )

    def __title_elo_label(self) -> tk.Label:
        """
        Builds an ELO Title Label
        """
        return tk.Label(
            self._elo_frame,
            text="Top World ELOs",
            font=("Arial", 30),
            bg="black",
            fg="white",
        )

    def __elo_label(self, rank: str, username: str, elo: str) -> tk.Label:
        """
        Builds an ELO label

        :param rank: What ELO rank the user is
        :param username: Username of ELO label
        :param elo: ELO to associate with user
        """
        return tk.Label(
            self._elo_frame,
            text=f"{rank.ljust(8, ' ')}| {username.ljust(40, ' ')}| {elo.ljust(6, ' ')}",
            font=("Arial", 12),
        )
