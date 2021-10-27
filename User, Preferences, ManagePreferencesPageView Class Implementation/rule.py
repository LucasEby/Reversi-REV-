from enum import Enum

class Rule(Enum):
    """
    An enum representing the two ruls.
    """
    A = "a"
    STANDARD = "standard"


    @staticmethod
    def has_rule(rule: str) -> bool:
        """
        Check if Rule contains certain rule.
        :param rule:    the name of rule to be checked in string
        :return:        true if the rule is included in Rule; false if not
        """
        try:
            Rule(rule)
            return True
        except ValueError:
            return False
