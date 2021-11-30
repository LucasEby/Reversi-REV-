import time
from typing import Tuple, Callable

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.game import Game
from client.server_comms.save_game_server_request import SaveGameServerRequest
from client.views.play_game_page_view import PlayGamePageView


class PlayGamePageController(HomeButtonPageController):

    _SAVE_GAME_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        go_home_callback: Callable[[], None],
        end_game_callback: Callable[[Game], None],
        game: Game,
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in-game
        :param go_home_callback: Callback to call when user requested going to the home screen
        :param end_game_callback: Callback to call after a game ended
        :param game: Game that was created to play the game with
        """
        super().__init__(go_home_callback=go_home_callback)
        self._task_execute_dict["place_tile"] = self.__execute_task_place_tile
        self._task_execute_dict["forfeit"] = self.__execute_task_forfeit
        self._end_game_callback: Callable[[Game], None] = end_game_callback
        self._game = game
        self._view = PlayGamePageView(
            game_obj=self._game,
            place_tile_cb=self.__handle_place_tile,
            forfeit_cb=self.__handle_forfeit,
        )

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
        # Try placing tile. If tile placement doesn't work, don't do anything.
        # Having no action occur on a click is enough feedback to user that their click is invalid
        try:
            valid_placement = self._game.place_tile(posn=coordinate)
        except Exception:
            valid_placement = False

        # Save game if it should be saved, waiting for save to be successful with a timeout
        if valid_placement is True:
            try:
                if self._game.save is True:
                    server_request: SaveGameServerRequest = SaveGameServerRequest(
                        self._game
                    )
                    server_request.send()
                    start_time: float = time.time()
                    while server_request.is_response_success() is None:
                        if time.time() - start_time > self._SAVE_GAME_TIMEOUT_SEC:
                            raise ConnectionError(
                                "Server unresponsive. Game could not be saved"
                            )
                    if server_request.is_response_success() is False:
                        raise ConnectionError("Server could not properly save game")
            except ConnectionError:
                # TODO: Notify view of server error
                valid_placement = True

        # If game is over, notify parent via callback
        if self._game.is_game_over():
            self._end_game_callback(self._game)
            return
        # Update view
        if valid_placement:
            self._view.update_game(game=self._game)
        self._view.display()

    def __execute_task_forfeit(self, task_info: int) -> None:
        """
        Takes action on player forfeit by communicating with model and updating view
        :param task_info: player_num (see __handle_forfeit)
        """
        player_num = task_info
        # Notify model who forfeited and notify parent game is over
        # self._game.forfeit(player_num)
        # self._end_game_callback(self._game)
