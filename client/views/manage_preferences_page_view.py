from typing import Callable, List
import tkinter as tk

from client.model.user import User
from client.model.colors import Color
from client.views.home_button_page_view import HomeButtonPageView
from client.model.preference import Preference


class ManagePreferencesPageView(HomeButtonPageView):
    """
    The class represents the view for Manage Preferences Page. It will display the preference choice for the given user.
    """

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        set_preferences_cb: Callable[[Preference], None],
        user: User,
    ) -> None:
        """
        Construct a new ManagePreferencesPageView with given user object.

        :param go_home_callback: Function to call when attempting to go home
        :param user: the user object
        :param set_preferences_cb: Function to call when going home
        """
        super().__init__(go_home_callback=go_home_callback)
        self._user = user
        self._color_options: List[str] = [
            Color.BLACK.value,
            Color.WHITE.value,
            Color.RED.value,
            Color.ORANGE.value,
            Color.YELLOW.value,
            Color.GREEN.value,
            Color.BLUE.value,
            Color.PURPLE.value,
        ]

        # Set up board size
        self._board_size_label = tk.Label(self._frame, text="Board size: ")
        self._board_size_var: tk.IntVar = tk.IntVar()
        self._board_size_box: tk.Spinbox = self.__board_size_spin_box(
            from_=4, to=20, increment=2, variable=self._board_size_var
        )

        # Set up board color
        self._board_color_label: tk.Label = tk.Label(self._frame, text="Board color: ")
        self._board_color_var: tk.StringVar = tk.StringVar()
        self._board_color_menu: tk.OptionMenu = self.__board_color(
            variable=self._board_color_var
        )

        # Set up user disk color
        self._your_disk_color_label: tk.Label = tk.Label(
            self._frame, text="Your Disk Color: "
        )
        self._main_user_disk_color_var: tk.StringVar = tk.StringVar()
        self._main_user_disk_color_menu: tk.OptionMenu = self.__main_user_disk_color(
            variable=self._main_user_disk_color_var
        )

        # Set up opp disk color
        self._opponent_disk_color_label: tk.Label = tk.Label(
            self._frame, text="Your opponent's Disk Color: "
        )
        self._opp_disk_color_var: tk.StringVar = tk.StringVar()
        self._opponent_disk_color_menu: tk.OptionMenu = self.__opponent_disk_color(
            variable=self._opp_disk_color_var
        )

        # Set up rules
        self._rule_options: List[str] = ["Standard"]
        self._change_rules_label = tk.Label(self._frame, text="Change Rules: ")
        self._change_rules_var: tk.StringVar = tk.StringVar()
        self._change_rules_menu: tk.OptionMenu = self.__change_rules(
            variable=self._change_rules_var
        )

        self._set_preferences_btn: tk.Button = self.__set_preferences()
        self._set_preferences_cb: Callable[[Preference], None] = set_preferences_cb
        self.display()

    def display(self) -> None:
        """
        Display the menu for preference. Initial page that display to the user.
        """
        super().display()
        self._board_size_label.pack()
        self._board_size_box.pack()
        self._board_color_label.pack()
        self._board_color_menu.pack()
        self._your_disk_color_label.pack()
        self._main_user_disk_color_menu.pack()
        self._opponent_disk_color_label.pack()
        self._opponent_disk_color_menu.pack()
        self._change_rules_label.pack()
        self._change_rules_menu.pack()
        self._set_preferences_btn.pack()

    def __board_size_spin_box(
        self, from_: float, to: float, increment: float, variable: tk.IntVar
    ) -> tk.Spinbox:
        """
        Creates a spinbox for the preferences page
        """
        variable.set(self._user.get_preference().get_board_size())
        return tk.Spinbox(
            self._frame,
            from_=from_,
            to=to,
            increment=increment,
            textvariable=variable,
        )

    def __board_color(self, variable: tk.StringVar) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable.set(self._user.get_preference().get_board_color())
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
        )

    def __main_user_disk_color(self, variable: tk.StringVar) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable.set(self._user.get_preference().get_my_disk_color())
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
        )

    def __opponent_disk_color(self, variable: tk.StringVar) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable.set(self._user.get_preference().get_opp_disk_color())
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
        )

    def __change_rules(self, variable: tk.StringVar) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable.set(str(self._user.get_preference().get_rule()))
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._rule_options,
        )

    def __set_preferences(self) -> tk.Button:
        """
        Builds the play different mode button
        """
        return tk.Button(
            self._frame,
            text="Set Preferences",
            width=25,
            height=5,
            bg="cyan",
            fg="black",
            command=self._handle_set_preferences,
        )

    def _handle_set_preferences(self):
        """
        Handles the operation of the preferences button.
        """
        new_pref: Preference = Preference()
        new_pref.set_board_size(self._board_size_var.get())
        new_pref.set_board_color(self._board_color_var.get())
        new_pref.set_my_disk_color(self._main_user_disk_color_var.get())
        new_pref.set_opp_disk_color(self._opp_disk_color_var.get())
        self._set_preferences_cb(new_pref)

    def destroy(self) -> None:
        """
        Destroy all widgets in this view
        """
        super().destroy()
        self._board_size_label.destroy()
        self._board_size_box.destroy()
        self._board_color_label.destroy()
        self._board_color_menu.destroy()
        self._your_disk_color_label.destroy()
        self._main_user_disk_color_menu.destroy()
        self._opponent_disk_color_label.destroy()
        self._opponent_disk_color_menu.destroy()
        self._change_rules_label.destroy()
        self._change_rules_menu.destroy()
        self._set_preferences_btn.destroy()
