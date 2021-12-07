from typing import Callable, List
import tkinter as tk

from client.model.user import User
from client.model.colors import Color
from client.views.home_button_page_view import HomeButtonPageView
from client.model.preference import Preference
from client.model.abstract_rule import AbstractRule
from client.model.standard_rule import StandardRule


class ManagePreferencesPageView(HomeButtonPageView):
    """
    The class represents the view for Manage Preferences Page. It will display the preference choice for the given user.
    """

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        user: User,
        set_preferences_cb: Callable[[Preference], None],
    ) -> None:
        """
        Construct a new ManagePreferencesPageView with given user object.

        :param go_home_callback: Function to call when attempting to go home
        :param user: the user object
        """
        super().__init__(go_home_callback=go_home_callback)
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
        self._rule_options: List[str] = ["Standard"]
        self._rule: AbstractRule = StandardRule()
        self._board_size_label = tk.Label(self._frame, text="Board size: ")
        self._board_size_box: tk.Spinbox = self.__board_size_spin_box(
            from_=4, to=12, increment=2
        )
        self._board_color_label = tk.Label(self._frame, text="Board color: ")
        self._board_color_menu: tk.OptionMenu = self.__board_color()
        self._your_disk_color_label = tk.Label(self._frame, text="Your Disk Color: ")
        self._main_user_disk_color_menu: tk.OptionMenu = self.__main_user_disk_color()
        self._opponent_disk_color_label = tk.Label(
            self._frame, text="Your opponent's Disk Color: "
        )
        self._opponent_disk_color_menu: tk.OptionMenu = self.__opponent_disk_color()
        self._change_rules_label = tk.Label(self._frame, text="Change Rules: ")
        self._change_rules_menu: tk.OptionMenu = self.__change_rules()
        self._set_preferences_btn: tk.Button = self.__set_preferences()
        self._user = user
        self._set_preferences_cb: Callable[[Preference], None] = set_preferences_cb
        self.new_preference = Preference()
        self.display()

    def display(self) -> None:
        """
        Display the menu for preference. Initial page that display to the user.
        """
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
        self, from_: float, to: float, increment: float
    ) -> tk.Spinbox:
        """
        Creates a spinbox for the preferences page
        """
        return tk.Spinbox(
            self._frame,
            from_=from_,
            to=to,
            increment=increment,
            command=lambda: self._handle_spinbox(self._board_size_box.get()),
        )

    def __board_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[3])
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
            command=lambda: self._handle_board_color(variable.get())
        )

    def __main_user_disk_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[4])
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
            command=lambda: self._handle_main_user_disk_color(variable.get())
        )

    def __opponent_disk_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[2])
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._color_options,
            command=lambda: self._handle_opponent_disk_color(variable.get())
        )

    def __change_rules(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._rule_options[0])
        return tk.OptionMenu(
            self._frame,
            variable,
            *self._rule_options,
            command=lambda: self._handle_rules(variable.get())
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

    def _handle_spinbox(self, board_size: int):
        """
        Handles the operations of the board size spinbox.
        """
        self._board_size = board_size

    def _handle_board_color(self, color: str):
        """
        Handles the operations of the board color option menu
        """
        self._board_color = color

    def _handle_main_user_disk_color(self, color: str):
        """
        Handles the operations of the main user disk color option menu
        """
        self._main_user_disk_color = color

    def _handle_opponent_disk_color(self, color: str):
        """
        Handles the operation of the opponent disk color option menu
        """
        self._opponent_disk_color = color

    def _handle_rules(self, chosen_rule: str):
        """
        Handles the operation of the rules option menu
        """
        self._rules = chosen_rule

    def _handle_set_preferences(self):
        """
        Handles the operation of the preferences button.
        """

        if self._rules == "StandardRule":
            self._chosen_rule: AbstractRule = StandardRule()
            self.new_preference.set_rule(self._chosen_rule)
        self.new_preference.set_opp_disk_color(
            self._convert_color(self._opponent_disk_color)
        )
        self.new_preference.set_my_disk_color(
            self._convert_color(self._main_user_disk_color)
        )
        self.new_preference.set_board_color(self._convert_color(self._board_color))
        self.new_preference.set_board_size(self._board_size)
        self._set_preferences_cb(self.new_preference)

    def destroy(self) -> None:
        """
        Destroy all widgets in this view
        """
        super().destroy()
        self._board_size_box.destroy()
        self._board_color_menu.destroy()
        self._main_user_disk_color_menu.destroy()
        self._opponent_disk_color_menu.destroy()
        self._change_rules_menu.destroy()

    @staticmethod
    def _convert_color(color: str) -> Color:
        """
        Used to convert the color strings into Color Enums

        :param color represents a color string
        """
        if color == "black":
            return Color.BLACK
        elif color == "white":
            return Color.WHITE
        elif color == "red":
            return Color.RED
        elif color == "orange":
            return Color.ORANGE
        elif color == "yellow":
            return Color.YELLOW
        elif color == "green":
            return Color.GREEN
        elif color == "blue":
            return Color.BLUE
        else:
            return Color.PURPLE
