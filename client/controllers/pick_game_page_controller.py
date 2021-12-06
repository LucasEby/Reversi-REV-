import random
import time
from typing import Callable, Optional

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.server_comms.create_game_server_request import CreateGameServerRequest
from client.server_comms.get_game_server_request import GetGameServerRequest
from client.views.pick_game_page_view import PickGamePageView
from client.model.user import User
from client.model.game_manager import GameManager
from client.model.player import Player
from client.model.ai import AI
from client.model.account import Account


class PickGamePageController(HomeButtonPageController):
    _CREATE_GAME_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        game_picked_callback: Callable[[GameManager], None],
        manage_preferences_callback: Callable[[User], None],
        main_user: User,
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in the "pick game"
        stage which is when the player chooses the type of game they wish to play.

        :param go_home_callback: Callback to call when user requested going to the home screen
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict[
            "local_single"
        ] = self.__execute_local_single_player_game
        self._task_execute_dict["local_multi"] = self.__execute_local_multiplayer_game
        self._task_execute_dict["online"] = self.__execute_online_game
        self._task_execute_dict[
            "manage_preferences"
        ] = self.__execute_change_preferences

        self._game_picked_callback: Callable[[GameManager], None] = game_picked_callback
        self._manage_preferences_callback: Callable[
            [User], None
        ] = manage_preferences_callback
        self._main_user: User = main_user
        self._view: PickGamePageView = PickGamePageView(
            self._handle_local_single_player_game,
            self._handle_local_multiplayer_game,
            self._handle_online_game,
            self._handle_change_preferences,
            go_home_callback=self.handle_home_button,
            username=self._main_user.get_username(),
        )

    def _handle_local_single_player_game(self) -> None:
        """
        Handles local single player game selection from user
        """
        self.queue(task_name="local_single")

    def _handle_local_multiplayer_game(self) -> None:
        """
        Handles local multiplayer game selection from user
        """
        self.queue(task_name="local_multi")

    def _handle_online_game(self) -> None:
        """
        Handles online game selection from user
        """
        self.queue(task_name="online_game")

    def _handle_change_preferences(self) -> None:
        """
        Handles change preferences selection from user
        """
        self.queue(task_name="manage_preferences")

    def __execute_local_single_player_game(self):
        """
        Create local single player game
        """
        self._view.destroy()
        ai: AI = AI()
        ai.set_difficulty(1)
        game_manager = GameManager(
            Player(self._main_user),
            ai,
            self._main_user,
            p1_first_move=bool(random.getrandbits(1)),
            save=isinstance(self._main_user, Account),
        )

        # Create game in database if main user is an account
        if isinstance(self._main_user, Account):
            self.__create_game_in_database(game_manager)

        self._game_picked_callback(game_manager)

    def __execute_local_multiplayer_game(self):
        """
        Create local multiplayer game
        """
        self._view.destroy()
        game_manager = GameManager(
            Player(self._main_user),
            Player(user=User(username="Guest")),
            self._main_user,
            p1_first_move=bool(random.getrandbits(1)),
            save=isinstance(self._main_user, Account),
        )

        # Create game in database if player 1 has an account
        if isinstance(self._main_user, Account):
            self.__create_game_in_database(game_manager)

        self._game_picked_callback(game_manager)

    def __execute_online_game(self):
        """
        Create online game
        :return:
        """
        self._view.destroy()
        # TODO: Do similar queue as above but add the matchmaker into it somehow
        # need to incorporate the MatchMakerRequest class when it is made.

    def __execute_change_preferences(self) -> None:
        """
        Notifies upper level that preferences should be changed
        """
        self._manage_preferences_callback(self._main_user)

    def __create_game_in_database(self, game_manager: GameManager) -> None:
        """
        Create an entry for the given game in the database. Uses a timeout.

        :param game_manager: The Game Manager to create with
        """
        try:
            server_request: CreateGameServerRequest = CreateGameServerRequest(game_manager=game_manager)
            server_request.send()
            start_time: float = time.time()
            while server_request.is_response_success() is None:
                if time.time() - start_time > self._CREATE_GAME_TIMEOUT_SEC:
                    raise ConnectionError(
                        "Server unresponsive. Game could not be created"
                    )
            if server_request.is_response_success() is False:
                raise ConnectionError("Server could not properly create game")
        except ConnectionError as e:
            # TODO: Notify view of server error
            print(e)

    def __get_saved_game_for_resuming(self) -> Optional[Game]:
        if isinstance(self._main_user, Account):
            try:
                server_request: GetGameServerRequest = GetGameServerRequest(self._main_user.id, True)
                server_request.send()
                start_time: float = time.time()
                while server_request.is_response_success() is None:
                    if time.time() - start_time > self._CREATE_GAME_TIMEOUT_SEC:
                        raise ConnectionError(
                            "Server unresponsive. Game could not be retrieved"
                        )
                if server_request.is_response_success() is False:
                    raise ConnectionError("Server could not properly retrieve game")
                else:
                    return server_request.get_game()
            except ConnectionError as e:
                # TODO: Notify view of server error
                print(e)