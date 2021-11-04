from typing import Tuple, Optional, Callable

from client.model.colors import Color
from client.views.manage_preferences_page_view import ManagePreferencesPageView
from client.model.preference import Preference
from client.model.rule import Rule
from client.model.user import User
from client.controllers.home_button_page_controller import HomeButtonPageController


class ManagePreferencesPageController(HomeButtonPageController):
    """
    This class represents a controller for Manage Preferences Page. It outputs to the view for Manage Preferences Page.
    It also takes input and make changes to the user's preference setting accordingly.
    """

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        end_home_callback: Callable[[], None],
        user: User
    ) -> None:
        """
        Construct the controller with a view for the passed in user
        :param user:    the user who is interacting with Manage Preferences Page
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict["board_size"] = self.__execute_change_board_size
        self._task_execute_dict["board_color"] = self.__execute_change_board_color
        self._task_execute_dict["my_disk_color"] = self.__execute_change_my_disk_color
        self._task_execute_dict["opp_disk_color"] = self.__execute_change_opp_disk_color
        self._task_execute_dict["line_color"] = self.__execute_change_line_color
        self._task_execute_dict["rule"] = self.__execute_change_rule
        self._task_execute_dict["tile_move_confirmation"] = self.__execute_change_tile_move_confirmation
        # execute stuffs
        self._end_game_callback: Callable[[], None] = end_home_callback
        self.__user: User = user
        self.__view: ManagePreferencesPageView = ManagePreferencesPageView(user)
        self.__preference: Preference = user.get_preference()

    def pref_go(self) -> None:
        """
        Run the controller to print out instruction menu, ask for input, and make changes to the preference setting
        accordingly if valid.
        """
        q: bool = False  # record for exit or not

        while not q:
            self.__view.display()
            pref_to_change: str = input(
                "According to the menu, enter 0-7 to change setting or exit:\n"
            )

            # check input validity instruction choice
            while not pref_to_change.isdigit() or int(pref_to_change) > 7:
                pref_to_change: str = input(
                    "Invalid instruction choice, please enter again: "
                )

            instruction: int = int(pref_to_change)
            if instruction == 0:
                self.__execute_change_board_size()
            elif instruction == 1:
                self.__execute_change_board_color()
            elif instruction == 2:
                self.__execute_change_my_disk_color()
            elif instruction == 3:
                self.__execute_change_opp_disk_color()
            elif instruction == 4:
                self.__execute_change_line_color()
            elif instruction == 5:
                self.__execute_change_rule()
            elif instruction == 6:
                self.__execute_change_tile_move_confirmation()
            elif instruction == 7:
                q = True

        quit()  # connect back to page machine?

    def __handle_change_board_size(self, size: int) -> None:
        """
        Handles board size change request from the user by queueing task
        :param size: the size of the board that the user want to set
        """
        self.queue(task_name="board_size", task_info=size)

    def ___handle_change_board_color(self, color: str) -> None:
        """
        Handles board color change request from the user by queueing task
        :param color: the color of the board that the user want to set
        """
        self.queue(task_name="board_color", task_info=color)

    def ___handle_change_my_disk_color(self, color: str) -> None:
        """
        Handles my disk color change request from the user by queueing task
        :param color: the color for my disk that the user want to set
        """
        self.queue(task_name="my_disk_color", task_info=color)

    def ___handle_change_opp_disk_color(self, color: str) -> None:
        """
        Handles opponent's disk color change request from the user by queueing task
        :param color: the size for opponent's disk that the user want to set
        """
        self.queue(task_name="opp_disk_color", task_info=color)

    def ___handle_change_line_color(self, color: str) -> None:
        """
        Handles line color change request from the user by queueing task
        :param color: the color of the line on the board that the user want to set
        """
        self.queue(task_name="line_color", task_info=color)

    def ___handle_change_rule(self, rule: str) -> None:
        """
        Handles game rule change request from the user by queueing task
        :param rule: the rule of the game that the user want to set
        """
        self.queue(task_name="ruler", task_info=rule)

    def ___handle_change_tile_move_confirmation(self, confirm: str) -> None:
        """
        Handles tile move confirmation change request from the user by queueing task
        :param confirm: whether the user wants to have a tile move confirmation
        """
        self.queue(task_name="tile_move_confirmation", task_info=confirm)

    def __execute_change_board_size(self, task_info: int) -> None:
        """
        Change the board size with user input. If the input number is not a number, negative, or odd, re-enter will be
        required.
        """
        # self.__view.display_board_size()  # print out the board size before change
        # size: str = input("Enter an integer for the new board size: ")

        # check input validity (.isdigit() makes sure size is a non-negative integer)
        while not task_info.isdigit() or int(task_info) % 2 != 0:
            size = input("Invalid board size, please enter again: ")

        new_board_size: int = int(task_info)
        self.__preference.set_board_size(new_board_size)  # chang the board size
        # self.__view.display_board_size()  # print out the board size before change

    def __execute_change_board_color(self, task_info: str) -> None:
        """
        Change the board color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        # self.__view.display_board_color()  # print out the board color before change
        # color: str = input("Enter the new board color: ")

        # check input validity
        task_info = self.__check_color_validity(task_info)

        # change the board color and check redundancy
        while not self.__preference.set_board_color(Color(task_info.lower())):
            task_info = input(
                "Entered board color conflicted with other components, please re-enter a new board color: "
            )
            task_info = self.__check_color_validity(task_info)

        # self.__view.display_board_color()  # print out the board color before change

    def __execute_change_my_disk_color(self, task_info: str) -> None:
        """
        Change my disk color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        # self.__view.display_my_disk_color()  # print out my disk color before change
        # color: str = input("Enter the new disk color for yourself: ")

        # check input validity
        task_info = self.__check_color_validity(task_info)

        # change the board color and check redundancy
        while not self.__preference.set_my_disk_color(Color(task_info.lower())):
            task_info = input(
                "Entered my disk color conflicted with other components, please re-enter a new disk color: "
            )
            task_info = self.__check_color_validity(task_info)

        # self.__view.display_my_disk_color()  # print out my disk color after change

    def __execute_change_opp_disk_color(self, task_info: str) -> None:
        """
        Change opponent's disk color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        # self.__view.display_opp_disk_color()  # print out opponent's disk color before change
        # color: str = input("Enter the new disk color for your opponent: ")

        # check input validity
        task_info = self.__check_color_validity(task_info)

        # change opponent's disk color and check redundancy
        while not self.__preference.set_opp_disk_color(Color(task_info.lower())):
            task_info = input(
                "Entered opponent's disk color conflicted with other components, please re-enter a new disk"
                + " color: "
            )
            task_info = self.__check_color_validity(task_info)

        # self.__view.display_opp_disk_color()  # print out opponent's disk color after change

    def __execute_change_line_color(self, task_info: str) -> None:
        """
        Change the line color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        # self.__view.display_line_color()  # print out line color before change
        # color: str = input("Enter the new line color: ")

        # check input validity
        task_info = self.__check_color_validity(task_info)

        # change the line color and check redundancy
        while not self.__preference.set_line_color(Color(task_info.lower())):
            task_info = input(
                "Entered line color conflicted with other components, please re-enter a new line color: "
            )
            task_info = self.__check_color_validity(task_info)

        # self.__view.display_line_color()  # print out line color after change

    def __execute_change_rule(self, task_info: str) -> None:
        """
        Change the rule with user's choice. If the input is not a color available, re-enter will be required.
        """
        # self.__view.display_rule()  # print out rule before change
        # rule: str = input("Enter your rule choice: ")

        # check input validity
        while not task_info.isalpha() or not Rule.has_rule(
            task_info.lower()
        ):  # changes needed with Rule implemented
            task_info = input("Invalid rule, please enter again: ")

        self.__preference.set_rule(Rule(task_info.lower()))  # change the rule
        # self.__view.display_rule()  # print out rule after change

    def __execute_change_tile_move_confirmation(self, task_info: str) -> None:
        """
        Change the tile move confirmation status with user's choice. If the input is invalid, re-enter will be required.
        """
        # self.__view.display_tile_move_confirmation()  # print out tile move confirmation before change
        # status: str = input("Turn on or off tile move confirmation (0: OFF; 1: ON): ")

        # check input validity
        while not task_info.isdigit() or int(task_info) > 1:
            task_info = input(
                "Invalid tile move confirmation status, please enter again (0: OFF; 1: ON): "
            )

        # change the tile move confirmation validity accordingly
        if int(task_info) == 0:
            self.__preference.set_tile_move_confirmation(False)
        elif int(task_info) == 1:
            self.__preference.set_tile_move_confirmation(True)

        self.__view.display_tile_move_confirmation()  # print out tile move confirmation before change

    @staticmethod
    def __check_color_validity(color: str) -> str:
        """
        Check if the input color is valid and ask for re-enter if invalid.
        :param color:   the input color name in string
        :return:        the valid color name in string
        """
        while not color.isalpha() or not Color.has_color(color.lower()):
            color = input("Input color invalid, please enter again: ")

        return color


#TODO:Changes in execute might be needed for re-enter to cooperate with the GUI?