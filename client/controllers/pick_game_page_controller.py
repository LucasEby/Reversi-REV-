from typing import Callable

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.game import Game
from client.views.pick_game_page_view import PickGamePageView
from client.model.user import User


class PickGamePageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
            user1: User,
            user2: User
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in the "pick game"
        stage which is when the player chooses the type of game they wish to play.
        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        super().__init__(go_home_callback=go_home_callback)
        self._user1 = user1
        self._user2 = user2
        self._view = PickGamePageView()

    def __handle_local_single_player_game(self) -> None:
        """
        Handles local AI selection from user by creating a local game with an AI
        Sets up the game with AI components
        """
        self.game_obj = Game(self._user1, self._user2, True, False)
        self._view.display_local_single_player_game_chosen()
        #TODO:
        # Incorporate AI levels. I wasn't sure if we were going to make a separate
        # page for it or if we would just have say 5 buttons on the screen (online, local vs User,
        # local vs easy AI, local vs medium AI, and local vs hard AI)?
        # I will incorporate the AI here once we've made the AI class.

    def __handle_local_multiplayer_game(self) -> None:
        """
        Handles local user selection from user by creating a local game with a user and a guest
        """
        self.game_obj = Game(self._user1, self._user2, True, False)
        self._view.display_local_multiplayer_game_chosen()

    def __handle_online_game(self) -> None:
        """
        Handles online user selection from user by creating an online game with another user
        """
        self.game_obj = Game(self._user1, self._user2, True, True)
        self._view.display_online_game_chosen()
        #TODO:
        # need to incorporate the MatchMakerRequest class when it is made.
        # def __handle_match_found(self, user: User) -> None:
        # comment description for the function:
        # "Handles online user selection from user by creating an online game with an AI"
