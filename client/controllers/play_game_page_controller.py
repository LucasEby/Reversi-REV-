from typing import Tuple, Optional, Callable

from client.controllers.home_button_page_controller import HomeButtonPageController


class PlayGamePageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        end_game_callback: Callable[[], None],
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in-game
        :param go_home_callback: Callback to call when user requested going to the home screen
        :param end_game_callback: Callback to call after a game ended
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict["place_tile"] = self.__execute_task_place_tile
        self._task_execute_dict["forfeit"] = self.__execute_task_forfeit
        self._end_game_callback: Callable[[], None] = end_game_callback

    def __handle_place_tile(self, coordinate: Tuple[int, int]) -> None:
        """
        Handles tile placement action from the user by queueing task
        :param coordinate: Coordinate on board (down, right) where tile placement was attempted
        """
        self.queue(task_name="place_tile", task_info=coordinate)

    def __handle_forfeit(self, player_num: int) -> None:
        """
        Handles forfeit action from user by queueing task
        :param player_num: Player number who forfeited
        """
        self.queue(task_name="forfeit", task_info=player_num)

    def __execute_task_place_tile(self, task_info: Tuple[int, int]) -> None:
        """
        Takes action on tile placement by communicating with model and updating view
        :param task_info: coordinate (see __handle_place_tile)
        """
        coordinate = task_info
        # TODO: Use coordinate with the game
        # TODO: Update view given result of game knowledge

    def __execute_task_forfeit(self, task_info: int) -> None:
        """
        Takes action on player forfeit by communicating with model and updating view
        :param task_info: player_num (see __handle_forfeit)
        """
        player_num = task_info
        # TODO: Use player num with the game
        # TODO: Update view given result of game knowledge
