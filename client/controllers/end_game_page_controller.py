from typing import Callable

from client.controllers.base_page_controller import BasePageController
from client.views.end_game_page_view import EndGamePageView


class EndGamePageController(BasePageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        rematch_callback: Callable[[], None],
        play_again_callback: Callable[[], None],
        Game,
        window
    ) -> None:

        """
        Specific type of page controller with a home button already handled.
        Many pages could have a home button, so this removes duplicate code.
        :param go_home_callback: Callback to call when going to the home screen
        """
        super().__init__()
        
        self.__go_home_callback: Callable[[],None] = go_home_callback
        self._rematch_callback: Callable[[], None] = rematch_callback
        self._play_again_callback: Callable[[], None] = play_again_callback
        self._task_execute_dict["rematch_button"] = self.__execute_task_rematch_button
        self._task_execute_dict["play_again_button"] = self.__execute_task_play_again_button
        self._window = window
        self._game = Game

        self.__view = EndGamePageView(self,
        self.__go_home_callback,
        Game,
        self._rematch_callback,
        self._play_again_callback,
        window)

    def __handle_rematch_button(self) -> None:
        """
        Handles rematch button action from the user by queueing task
        """
        #TODO: Rematch builds a new game functioanlity 
        self.queue(task_name="rematch_button")

    def __handle_play_again(self) -> None:
        """
        Handles play again button action from the user by queueing task
        """
        self.queue(task_name="play_again")
    
    def __execute_task_rematch_button(self) -> None:
        self._rematch_callback()
        #TODO: Rematch builds a new game functioanlity 

    def __execute_task_play_again_button(self) -> None:
        """
        Handles play again button action from the user by queueing task
        """
        self._play_again_callback()
        

   