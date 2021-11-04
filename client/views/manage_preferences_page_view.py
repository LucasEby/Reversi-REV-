from client.model.preference import Preference
from client.model.user import User


class ManagePreferencesPageView:
    """
    The class represents the view for Manage Preferences Page. It will display the preference choice for the given user.
    """

    def __init__(self, user: User) -> None:
        """
        Construct a new ManagePreferencesPageView with given user object.

        :param user: the user object
        """
        self.__user: User = user
        self.__preference: Preference = self.__user.get_preference()

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
            "My opponent's current disk color: " + self.__preference.get_opp_disk_color()
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
        print("Current rule: " + self.__preference.get_rule())

    def display_tile_move_confirmation(self) -> None:
        """
        Display the current tile move confirmation status.
        """
        if self.__preference.get_tile_move_confirmation():
            print("Current tile move confirmation: On")
        else:
            print("Current tile move confirmation: Off")

    @staticmethod
    def display() -> None:
        """
        Display the menu for preference. Initial page that display to the user.
        """
        print("Here are the options for your preference:")
        print("0. Change board size")
        print("1. Change board color")
        print("2. Change my disk color")
        print("3. Change opponent's disk color")
        print("4. Change line color")
        print("5. Change rule")
        print("6. Set tile move confirmation")
        print("7. Exit preference setting")
