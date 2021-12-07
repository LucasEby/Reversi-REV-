from typing import Callable
import tkinter as tk

from client.model.user import User
from client.model.colors import Color
from client.views.home_button_page_view import HomeButtonPageView


class ManagePreferencesPageView(HomeButtonPageView):
    """
    The class represents the view for Manage Preferences Page. It will display the preference choice for the given user.
    """

    def __init__(self,
                 go_home_callback: Callable[[], None],
                 user: User,
                 board_size_cb: Callable[[int], None],
                 board_color_cb: Callable[[str], None],
                 main_user_disk_color_cb: Callable[[str], None],
                 opponent_disk_color_cb: Callable[[str], None],
                 rules_cb: Callable[[str], None],
                 set_preferences_cb: Callable[[], None]
        ) -> None:
        """
        Construct a new ManagePreferencesPageView with given user object.

        :param go_home_callback: Function to call when attempting to go home
        :param user: the user object
        """
        super().__init__(go_home_callback=go_home_callback)
        self._color_options: [tk.StringVar] = [Color[0].value, Color[1].value, Color[2].value, Color[3].value,
                                              Color[4].value, Color[5].value, Color[6].value, Color[7].value]
        self._rule_options: [tk.StringVar] = ["Standard"]
        self._board_size_box: tk.Spinbox = self.__board_size_spin_box(from_=4, to=12, increment=2)
        self._board_color_menu: tk.OptionMenu = self.__board_color()
        self._main_user_disk_color_menu: tk.OptionMenu = self.__main_user_disk_color()
        self._opponent_disk_color_menu: tk.OptionMenu = self.__opponent_disk_color()
        self._change_rules_menu: tk.OptionMenu = self.__change_rules()

        self._user = user
        self._board_size_cb: Callable[[int], None] = board_size_cb
        self._board_color_cb: Callable[[str], None] = board_color_cb
        self._main_user_disk_color_cb: Callable[[str], None] = main_user_disk_color_cb
        self._opponent_disk_color_cb: Callable[[str], None] = opponent_disk_color_cb
        self._rules_cb: Callable[[str], None] = rules_cb
        self._set_preferences_cb: Callable[[], None] = set_preferences_cb
        self.display()

    def display(self) -> None:
        """
        Display the menu for preference. Initial page that display to the user.
        """
        self._board_size_box.pack()
        self._board_color_menu.pack()
        self._main_user_disk_color_menu.pack()
        self._opponent_disk_color_menu.pack()
        self._change_rules_menu.pack()

    def __board_size_spin_box(self, from_: float, to: float, increment: float) -> tk.Spinbox:
        """
        Creates a spinbox for the preferences page
        """
        return tk.Spinbox(self._frame, from_=from_, to=to, incement=increment,
                          command=lambda: self._handle_spinbox(self._board_size_box.get()))

    def __board_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[3])
        return tk.OptionMenu(self._frame, variable, *self._color_options,
                             command=lambda: self._handle_board_color(variable.get()))

    def __main_user_disk_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[4])
        return tk.OptionMenu(self._frame, variable, *self._color_options,
                             command=lambda: self._handle_main_user_disk_color(variable.get()))

    def __opponent_disk_color(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[2])
        return tk.OptionMenu(self._frame, variable, *self._color_options,
                             command=lambda: self._handle_opponent_disk_color(variable.get()))

    def __change_rules(self) -> tk.OptionMenu:
        """
        Creates an option menu to give the user the choice of a wide variety of options
        """
        variable = tk.StringVar()
        variable.set(self._color_options[0])
        return tk.OptionMenu(self._frame, variable, *self._color_options,
                             command=lambda: self._handle_rules(variable.get()))

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
        self._board_size_cb(board_size)

    def _handle_board_color(self, color: str):
        self._board_color_cb(color)

    def _handle_main_user_disk_color(self, color: str):
        self._main_user_disk_color_cb(color)

    def _handle_opponent_disk_color(self, color: str):
        self._opponent_disk_color_cb(color)

    def _handle_rules(self, chosen_rule: str):
        self._rules_cb(chosen_rule)

    def _handle_set_preferences(self):
        self._set_preferences_cb()

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
