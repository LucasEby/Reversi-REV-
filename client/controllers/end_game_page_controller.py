from typing import Callable, Optional
import time

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.account import Account
from client.model.calculate_new_elos import CalculateNewELOs
from client.model.user import User
from client.server_comms.create_game_server_request import CreateGameServerRequest
from client.server_comms.update_elo_server_request import UpdateELOServerRequest
from client.views.end_game_page_view import EndGamePageView
from client.model.game_manager import GameManager
from client.model.player import Player


class EndGamePageController(HomeButtonPageController):
    _SERVER_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        play_again_callback: Callable[[GameManager], None],
        play_different_mode_callback: Callable[[User], None],
        game_manager: GameManager,
    ) -> None:
        """
        Page controller to handle the next steps after a game ends

        :param go_home_callback: Callback to call when going to the home screen
        :param play_again_callback: Callback to call when attempting to play same game mode
        :param play_different_mode_callback: Callback to call when user wants to play different game mode
        :param game_manager: Contains the Game that was just ended and the primary user of the application
        """
        super().__init__(go_home_callback=go_home_callback)

        self._play_again_callback: Callable[[GameManager], None] = play_again_callback
        self._play_different_mode_callback: Callable[
            [User], None
        ] = play_different_mode_callback
        self._game_manager: GameManager = game_manager
        self._main_user: User = self._game_manager.main_user
        self.__update_elos(self._game_manager)

        self._task_execute_dict["play_again"] = self.__execute_task_play_again
        self._task_execute_dict[
            "play_different_mode"
        ] = self.__execute_task_play_different_mode

        self._view = EndGamePageView(
            go_home_cb=self.handle_home_button,
            play_again_cb=self.__handle_play_again,
            play_different_mode_cb=self.__handle_play_different_mode,
            game_manager=game_manager,
        )

    def __update_elos(self, game_manager: GameManager) -> None:
        user1: User = game_manager.get_player1().get_user()
        user2: User = game_manager.get_player2().get_user()
        if user1 is None or user2 is None:
            return
        p1_won: bool = game_manager.game.get_winner() == 1
        if isinstance(user1, Account) and isinstance(user2, Account):
            if user1.id is None or user2.id is None:
                return
            updated_elos = CalculateNewELOs.get_new_elos(
                user1.id, user1.elo, user2.id, user2.elo, p1_won
            )
            p1_id: int = updated_elos[0][0]
            p1_new_elo: int = updated_elos[0][1]
            p2_id: int = updated_elos[1][0]
            p2_new_elo: int = updated_elos[1][1]
            # Update ELOs, waiting for database call to be successful with a timeout
            try:
                # Update player 1's ELO
                server_request1: UpdateELOServerRequest = UpdateELOServerRequest(
                    p1_id, p1_new_elo
                )
                server_request1.send()
                start_time: float = time.time()
                while server_request1.is_response_success() is None:
                    if time.time() - start_time > self._SERVER_TIMEOUT_SEC:
                        raise ConnectionError(
                            "Server unresponsive. P1 ELO could not be updated"
                        )
                if server_request1.is_response_success() is False:
                    raise ConnectionError("Server could not properly update P1 ELO")
                # Update player 2's ELO
                server_request2: UpdateELOServerRequest = UpdateELOServerRequest(
                    p2_id, p2_new_elo
                )
                server_request2.send()
                start_time = time.time()
                while server_request2.is_response_success() is None:
                    if time.time() - start_time > self._SERVER_TIMEOUT_SEC:
                        raise ConnectionError(
                            "Server unresponsive. P2 ELO could not be updated"
                        )
                if server_request2.is_response_success() is False:
                    raise ConnectionError("Server could not properly update P2 ELO")
            except ConnectionError as e:
                # TODO: Notify view of server error
                print(e)

    def __handle_play_again(self) -> None:
        """
        Handles play again button action from the user by queueing task
        """
        self.queue(task_name="play_again")

    def __handle_play_different_mode(self) -> None:
        """
        Handles play different mode button action from the user by queueing task
        """
        self.queue(task_name="play_different_mode")

    def __execute_task_play_again(self) -> None:
        """
        Creates game to play again with
        """
        self._view.destroy()
        old_p1: Player = self._game_manager.get_player1()
        old_p2: Player = self._game_manager.get_player2()
        new_game_manager = GameManager(
            player1=old_p1,
            player2=old_p2,
            main_user=self._main_user,
            save=self._game_manager.game.save,
        )

        # Create game in database if necessary
        if new_game_manager.game.save:
            try:
                server_request: CreateGameServerRequest = CreateGameServerRequest(
                    game_manager=new_game_manager
                )
                server_request.send()
                start_time: float = time.time()
                while server_request.is_response_success() is None:
                    if time.time() - start_time > self._SERVER_TIMEOUT_SEC:
                        raise ConnectionError(
                            "Server unresponsive. Game could not be created"
                        )
                if server_request.is_response_success() is False:
                    raise ConnectionError("Server could not properly create game")
                game_id: Optional[int] = server_request.get_game_id()
                if game_id is not None:
                    new_game_manager.game.set_id(game_id)
            except ConnectionError as e:
                # TODO: Notify view of server error
                print(e)

        self._play_again_callback(new_game_manager)

    def __execute_task_play_different_mode(self) -> None:
        """
        Notifies upper level to play different game mode
        """
        self._view.destroy()
        self._play_different_mode_callback(self._main_user)
