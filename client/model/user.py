from client.model.preference import Preference


class User:
    """
    This class represents a user with an ID number, a username, and one's preference setting.
    """

    def __init__(self, username: str) -> None:
        """
        Construct a user with username, and initialize the preference object.
        :param username:    the username of the user
        """
        self.__username: str = username
        self.__preference: Preference = Preference()

    def get_username(self) -> str:
        """
        Get the username of the user.
        :return:    a string for the username
        """
        return self.__username

    def get_preference(self) -> Preference:
        """
        Get the preference settings for the user.
        :return:    the preference for the user
        """
        return self.__preference

    # def set_preferences(preference: Preference) -> None:
