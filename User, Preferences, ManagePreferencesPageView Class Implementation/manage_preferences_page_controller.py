from colors import Color
from manage_preferences_page_view import ManagePreferencesPageView
from rule import Rule
from user import User


class ManagePreferencesPageController:
    """
    This class represents a controller for Manage Preferences Page. It outputs to the view for Manage Preferences Page.
    It also takes input and make changes to the user's preference setting accordingly.
    """
    def __init__(self, user: User) -> None:
        """
        Construct the controller with a view for the passed in user
        :param user:    the user who is interacting with Manage Preferences Page
        """
        self.__user = user
        self.__view = ManagePreferencesPageView(user)
        self.__preference = user.get_preference()


    def pref_go(self) -> None:
        """
        Run the controller to print out instruction menu, ask for input, and make changes to the preference setting
        accordingly if valid.
        """
        q = False   # record for exit or not
    
        while not q:
            self.__view.print_menu()
            pref_to_change = input("According to the menu, enter 0-7 to change setting or exit:\n")
            
            # check input validity instruction choice
            while not pref_to_change.isdigit() or int(pref_to_change) > 7:
                pref_to_change = input("Invalid instruction choice, please enter again: ")

            instruction = int(pref_to_change)
            if instruction == 0:
                self.__change_board_size()
            elif instruction == 1:
                self.__change_board_color()
            elif instruction == 2:
                self.__change_my_disk_color()
            elif instruction == 3:
                self.__change_opp_disk_color()
            elif instruction == 4:
                self.__change_line_color()
            elif instruction == 5:
                self.__change_rule()
            elif instruction == 6:
                self.__change_tile_move_confirmation()
            elif instruction == 7:
                q = True

        quit()


    def __change_board_size(self) -> None:
        """
        Change the board size with user input. If the input number is not a number, negative, or odd, re-enter will be
        required.
        """
        self.__view.print_board_size()  # print out the board size before change
        size = input("Enter an integer for the new board size: ")

        # check input validity (.isdigit() makes sure size is a non-negative integer)
        while not size.isdigit() or int(size) % 2 != 0:
            size = input("Invalid board size, please enter again: ")
        
        new_board_size = int(size)
        self.__preference.set_board_size(new_board_size)    # chang the board size
        self.__view.print_board_size()  # print out the board size before change


    def __change_board_color(self) -> None:
        """
        Change the board color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        self.__view.print_board_color() # print out the board color before change
        color = input("Enter the new board color: ")

        # check input validity
        color = self.__check_color_validity(color)

        # change the board color and check redundancy
        while not self.__preference.set_board_color(Color(color.lower())):
            color = input("Entered board color conflicted with other components, please re-enter a new board color: ")
            color = self.__check_color_validity(color)

        self.__view.print_board_color() # print out the board color before change

    
    def __change_my_disk_color(self) -> None:
        """
        Change my disk color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        self.__view.print_my_disk_color()   # print out my disk color before change
        color = input("Enter the new disk color for yourself: ")

        # check input validity
        color = self.__check_color_validity(color)

        # change the board color and check redundancy
        while not self.__preference.set_my_disk_color(Color(color.lower())):
            color = input("Entered my disk color conflicted with other components, please re-enter a new disk color: ")
            color = self.__check_color_validity(color)

        self.__view.print_my_disk_color()   # print out my disk color after change


    def __change_opp_disk_color(self) -> None:
        """
        Change opponent's disk color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        self.__view.print_opp_disk_color()  # print out opponent's disk color before change
        color = input("Enter the new disk color for your opponent: ")

        # check input validity
        color = self.__check_color_validity(color)

        # change opponent's disk color and check redundancy
        while not self.__preference.set_opp_disk_color(Color(color.lower())):
            color = input("Entered opponent's disk color conflicted with other components, please re-enter a new disk"
                          + " color: ")
            color = self.__check_color_validity(color)

        self.__view.print_opp_disk_color()  # print out opponent's disk color after change


    def __change_line_color(self) -> None:
        """
        Change the line color with user's choice. If the input is not a color available or redundant with other
        components, re-enter will be required.
        """
        self.__view.print_line_color()  # print out line color before change
        color = input("Enter the new line color: ")

        # check input validity
        color = self.__check_color_validity(color)

        # change the line color and check redundancy
        while not self.__preference.set_line_color(Color(color.lower())):
            color = input("Entered line color conflicted with other components, please re-enter a new line color: ")
            color = self.__check_color_validity(color)

        self.__view.print_line_color()  # print out line color after change


    def __change_rule(self) -> None:
        """
        Change the rule with user's choice. If the input is not a color available, re-enter will be required.
        """
        self.__view.print_rule()    # print out rule before change
        rule = input("Enter your rule choice: ")

        # check input validity
        while not rule.isalpha() or not Rule.has_rule(rule.lower()): # changes needed with Rule implemented
            rule = input("Invalid rule, please enter again: ")
        
        self.__preference.set_rule(Rule(rule.lower()))  # change the rule
        self.__view.print_rule()    # print out rule after change


    def __change_tile_move_confirmation(self) -> None:
        """
        Change the tile move confirmation status with user's choice. If the input is invalid, re-enter will be required.
        """
        self.__view.print_tile_move_confirmation()  # print out tile move confirmation before change
        status = input("Turn on or off tile move confirmation (0: OFF; 1: ON): ")

        # check input validity
        while not status.isdigit() or int(status) > 1:
            status = input("Invalid tile move confirmation status, please enter again (0: OFF; 1: ON): ")

        # change the tile move confirmation validity accordingly
        if int(status) == 0:
            self.__preference.set_tile_move_confirmation(False)
        elif int(status) == 1:
            self.__preference.set_tile_move_confirmation(True)

        self.__view.print_tile_move_confirmation()  # print out tile move confirmation before change


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

    
