from typing import Callable

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.views.pick_game_page_view import PickGamePageView
from client.model.game import Game
from client.model.user import User


class PickGamePageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        play_local_single_player_game_callback: Callable[[Game], None],
        play_local_multiplayer_game_callback: Callable[[Game], None],
        play_online_game_callback: Callable[[Game], None],
        manage_preferences_callback: Callable[[Game], None],
        main_user: User,
        window,
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in the "pick game"
        stage which is when the player chooses the type of game they wish to play.

        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        super().__init__(go_home_callback=go_home_callback)
        self._play_local_single_player_game_callback: Callable[
            [Game], None
        ] = play_local_single_player_game_callback
        self._play_local_multiplayer_game_callback: Callable[
            [Game], None
        ] = play_local_multiplayer_game_callback
        self._play_online_game_callback: Callable[
            [Game], None
        ] = play_online_game_callback
        self._manage_preferences_callback = manage_preferences_callback
        self._main_user = main_user
        self.__view = PickGamePageView(pgc=self, window=window)

    def run(self) -> None:
        self.__view.start_gui()

    def handle_change_preferences(self) -> None:
        """
        Handles local user selection from user by creating a local game with a user and a guest

        :return: None
        """
        # self._manage_preferences_callback(self._game)
        print("change preferences")

    def handle_local_single_player_game(self) -> None:
        """
        Handles local AI selection from user by creating a local game with an AI
        Sets up the game with AI components

        :return: None
        """
        self.__view.display_local_single_player_game_chosen()
        # self._play_local_single_player_game_callback(Game(self._main_user, User(2, "Guest")))
        # TODO:
        # We need to incorporate the AI functionality here.
        # We need to also change "User(2, Guest) to be an AI

    def handle_local_multiplayer_game(self) -> None:
        """
        Handles local user selection from user by creating a local game with a user and a guest

        :return: None
        """
        self.__view.display_local_multiplayer_game_chosen()
        self._play_local_multiplayer_game_callback(
            Game(self._main_user, User(2, "Guest"))
        )
        # TODO:
        # play locally callback = self. play locally

    def handle_online_game(self) -> None:
        """
        Handles online user selection from user by creating an online game with another user

        :return: None
        """
        self.__view.display_online_game_chosen()
        # TODO:
        # need to incorporate the MatchMakerRequest class when it is made.
        # def __handle_match_found(self, user: User) -> None:
        # comment description for the function:
        # "Handles online user selection from user by creating an online game with an AI"
