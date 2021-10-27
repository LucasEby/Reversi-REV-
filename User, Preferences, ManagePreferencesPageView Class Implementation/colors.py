from enum import Enum


class Color(Enum):
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"

    @staticmethod
    def has_color(color: str) -> bool:
        """
        Check if Color contains certain color.
        :param color:   the name of the color to be checked in string
        :return:        true if the color is included in Color; false if not
        """
        try:
            Color(color)
            return True
        except ValueError:
            return False
