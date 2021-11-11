from client.views.base_page_view import BasePageView


class PickGamePageView(BasePageView):
    def __init__(
        self,
    ) -> None:
        """
        TODO:
        This will later initialize the Pick Game Page with a list of buttons.
        """
        super().__init__()

    def display(self) -> None:
        print("Game Options: \n")
        self.__display_local_single_player_game()
        self.__display_local_multiplayer_game()
        self.__display_online_game()

    def __display_local_single_player_game(self) -> None:
        """
        Notifies the user that a local user/guest vs AI game is a game option:
        """
        print("User/guest vs AI local game.\n")

    def display_local_single_player_game_chosen(self) -> None:
        """
        Confirms to the user that the local user/guest vs AI option was chosen.
        """
        print("User/guest vs AI local game was chosen.\n")

    def __display_local_multiplayer_game(self) -> None:
        """
        Notifies the user that a local user vs guest game is a game option:
        """
        print("User vs guest local game.\n")

    def display_local_multiplayer_game_chosen(self) -> None:
        """
        Confirms to the user that the local user vs guest option was chosen.
        """
        print("User vs guest online game was chosen.\n")

    def __display_online_game(self) -> None:
        """
        Notifies the user that a User vs user online game is a game option:
        """
        print("User vs user online game.\n")

    def display_online_game_chosen(self) -> None:
        """
        Confirms to the user that the online user vs user option was chosen.
        """
        print("User vs user online game was chosen.\n")
