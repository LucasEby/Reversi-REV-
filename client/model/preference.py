from client.model.abstract_rule import AbstractRule
from client.model.colors import Color
from client.model.standard_rule import StandardRule


class Preference:
    """
    The class represents the preferences for a signed in user. It stores the choice of different settings in the game.
    It also includes setters and getters to modify and get the preference choices.
    """

    def __init__(self) -> None:
        self.__board_size: int = 8
        self.__board_color: Color = Color.GREEN
        self.__my_disk_color: Color = Color.WHITE
        self.__opp_disk_color: Color = Color.BLACK
        self.__line_color: Color = Color.BLACK
        self.__rule: AbstractRule = StandardRule()
        self.__tile_move_confirmation: bool = True

    # setters and getters
    def set_board_size(self, size: int) -> None:
        """
        Set the board size.
        :param size:        the desired size of the board
        :raise ValueError:  if the given size is not even
        """
        if size % 2 != 0:
            raise ValueError("Size should be an even number")
        self.__board_size = size

    def get_board_size(self) -> int:
        """
        Get the size of the board.
        :return:    the size of the board
        """
        return self.__board_size

    def set_board_color(self, color: Color) -> bool:
        """
        Set the base color of the board.
        :param color:   color of the board base
        :return:        False if the color is the same as other components in the game; True if color changed
                        successfully
        """
        record: Color = self.__board_color
        self.__board_color = color

        # check redundancy
        if not self._check_color_validity():
            self.__board_color = record
            return False

        return True

    def get_board_color(self) -> str:
        """
        Get the color of the board.
        :return:    the color of the base board
        """
        return str(self.__board_color.value)

    def set_my_disk_color(self, color: Color) -> bool:
        """
        Set the disk color for the user oneself.
        :param color:   color of the user's disk
        :return:        False if the color is the same as other components in the game; True if color changed
                        successfully
        """
        record: Color = self.__my_disk_color
        self.__my_disk_color = color

        # check redundancy
        if not self._check_color_validity():
            self.__my_disk_color = record
            return False

        return True

    def get_my_disk_color(self) -> str:
        """
        Get the color of the disk using by the user.
        :return:    the color the user's disk
        """
        return str(self.__my_disk_color.value)

    def set_opp_disk_color(self, color: Color) -> bool:
        """
        Set the disk color for the opponent.
        :param color:   color of the opponent's disk
        :return:        False if the color is the same as other components in the game; True if color changed
                        successfully
        """
        record: Color = self.__opp_disk_color
        self.__opp_disk_color = color

        # check redundancy
        if not self._check_color_validity():
            self.__opp_disk_color = record
            return False

        return True

    def get_opp_disk_color(self) -> str:
        """
        Get the color of the disk shown on the board as opponent.
        :return:    the color of opponent's disk
        """
        return str(self.__opp_disk_color.value)

    def set_line_color(self, color: Color) -> bool:
        """
        Set the line color in the board.
        :param color:   color of the line in the board
        :return:        False if the color is the same as other components in the game; True if color changed
                        successfully
        """
        record: Color = self.__line_color
        self.__line_color = color

        # check redundancy
        if not self._check_color_validity():
            self.__line_color = record
            return False

        return True

    def get_line_color(self) -> str:
        """
        Get the color of the lines in the board.
        :return:    the color of the lines in the board
        """
        return str(self.__line_color.value)

    def set_rule(self, rule: AbstractRule) -> None:
        """
        Set the rule of the game to be either StandardRule or ARule.
        :param rule:    the type rule the user wants to have
        """
        self.__rule = rule

    def get_rule(self) -> AbstractRule:
        """
        Get the name of the rule that is set in the preference right now.
        :return:    the name of the rule in preference
        """
        return self.__rule

    def set_tile_move_confirmation(self, prompt: bool) -> None:
        """
        Set the tile move confirmation to either be ON or OFF.
        :param prompt:  user choice to turn ON or OFF the confirmation setting
        """
        self.__tile_move_confirmation = prompt

    def get_tile_move_confirmation(self) -> bool:
        """
        Get the current status of tile move confirmation either be ON or OFF.
        :return:    a boolean representing the status (0: OFF; 1: ON)
        """
        return self.__tile_move_confirmation

    def _check_color_validity(self) -> bool:
        """
        Check if the color settings are valid to avoid components in the same color that will worsen the visibility
        :return:    False if the there is repeated color for compoenents that will harm visibility; True if not
        """
        if (
            self.__board_color == self.__my_disk_color
            or self.__board_color == self.__opp_disk_color
        ):
            return False
        elif self.__board_color == self.__line_color:
            return False
        elif self.__my_disk_color == self.__opp_disk_color:
            return False

        return True
