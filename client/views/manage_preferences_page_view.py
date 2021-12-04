from typing import Callable

from client.model.preference import Preference
from client.model.user import User
from client.views.home_button_page_view import HomeButtonPageView


class ManagePreferencesPageView(HomeButtonPageView):
    """
    The class represents the view for Manage Preferences Page. It will display the preference choice for the given user.
    """

    def __init__(self, go_home_callback: Callable[[], None], user: User) -> None:
        """
        Construct a new ManagePreferencesPageView with given user object.

        :param go_home_callback: Function to call when attempting to go home
        :param user: the user object
        """
        super().__init__(go_home_callback=go_home_callback)
        self.__user: User = user
        self.__preference: Preference = self.__user.get_preference()
        self.display()

    def display_board_size(self) -> None:
        """
        Display the current board size.
        """
        print("Current board size: " + str(self.__preference.get_board_size()))

    def display_board_color(self) -> None:
        """
        Display the current board color.
        """
        print("Current board color: " + self.__preference.get_board_color())

    def display_my_disk_color(self) -> None:
        """
        Display the current disk color for oneself.
        """
        print("My current disk color: " + self.__preference.get_my_disk_color())

    def display_opp_disk_color(self) -> None:
        """
        Display the current disk color for opponent.
        """
        print(
            "My opponent's current disk color: "
            + self.__preference.get_opp_disk_color()
        )

    def display_line_color(self) -> None:
        """
        Display the current line color.
        """
        print("Current line color: " + self.__preference.get_line_color())

    def display_rule(self) -> None:
        """
        Display the current rule.
        """
        print("Current rule: " + str(self.__preference.get_rule()))

    def display_tile_move_confirmation(self) -> None:
        """
        Display the current tile move confirmation status.
        """
        if self.__preference.get_tile_move_confirmation():
            print("Current tile move confirmation: On")
        else:
            print("Current tile move confirmation: Off")

    def destroy(self) -> None:
        """
        Destroy all widgets in this view
        """
        pass

    def display(self) -> None:
        """
        Display the menu for preference. Initial page that display to the user.
        """
        print("Here are the options for your preference:")
        print("0. Change board size")
        self.display_board_size()
        print("1. Change board color")
        self.display_board_color()
        print("2. Change my disk color")
        self.display_my_disk_color()
        print("3. Change opponent's disk color")
        self.display_opp_disk_color()
        print("4. Change line color")
        self.display_line_color()
        print("5. Change rule")
        self.display_rule()
        print("6. Set tile move confirmation")
        self.display_tile_move_confirmation()
        print("7. Exit preference setting")
        # back to home page command
