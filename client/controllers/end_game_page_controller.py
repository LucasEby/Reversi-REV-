from typing import Callable

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.user import User
from client.views.end_game_page_view import EndGamePageView
from client.model.game import Game


class EndGamePageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        play_again_callback: Callable[[Game, User], None],
        play_different_mode_callback: Callable[[User], None],
        game: Game,
        main_user: User,
    ) -> None:
        """
        Page controller to handle the next steps after a game ends

        :param go_home_callback: Callback to call when going to the home screen
        :param play_again_callback: Callback to call when attempting to play same game mode
        :param play_different_mode_callback: Callback to call when user wants to play different game mode
        :param game: Game that was just ended
        :param main_user: Primary user of the application
        """
        super().__init__(go_home_callback=go_home_callback)

        self._play_again_callback: Callable[[Game, User], None] = play_again_callback
        self._play_different_mode_callback: Callable[
            [User], None
        ] = play_different_mode_callback
        self._game: Game = game
        self._main_user: User = main_user

        self._task_execute_dict["play_again"] = self.__execute_task_play_again
        self._task_execute_dict[
            "play_different_mode"
        ] = self.__execute_task_play_different_mode

        self._view = EndGamePageView(
            go_home_cb=go_home_callback,
            play_again_cb=self.__handle_play_again,
            play_different_mode_cb=self.__handle_play_different_mode,
            game=game,
        )

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
        self._play_again_callback(self._game, self._main_user)

    def __execute_task_play_different_mode(self) -> None:
        """
        Notifies upper level to play different game mode different mode with
        """
        self._view.destroy()
        self._play_different_mode_callback(self._main_user)