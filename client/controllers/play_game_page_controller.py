import time
from typing import Tuple, Callable

from client.controllers.base_page_controller import BasePageController
from client.model.game import Game
from client.model.user import User
from client.model.game_manager import GameManager
from client.server_comms.save_game_server_request import SaveGameServerRequest
from client.views.play_game_page_view import PlayGamePageView


class PlayGamePageController(BasePageController):

    _SAVE_GAME_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        end_game_callback: Callable[[GameManager], None],
        game_manager: GameManager,
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in-game
        :param end_game_callback: Callback to call after a game ended
        :param game: Game that was created to play the game with
        """
        super().__init__()
        self._task_execute_dict["place_tile"] = self.__execute_task_place_tile
        self._task_execute_dict["forfeit"] = self.__execute_task_forfeit

        self._end_game_callback: Callable[[GameManager], None] = end_game_callback
        self._game_manager: GameManager = game_manager
        self._game: Game = game_manager.game
        self._main_user: User = game_manager.main_user
        self._view: PlayGamePageView = PlayGamePageView(
            game_manager=self._game_manager,
            place_tile_cb=self.__handle_place_tile,
            forfeit_cb=self.__handle_forfeit,
            preferences=self._main_user.get_preference(),
        )

    def __handle_place_tile(self, coordinate: Tuple[int, int]) -> None:
        """
        Handles tile placement action from the user by queueing task

        :param coordinate: Coordinate on board (down, right) where tile placement was attempted
        """
        self.queue(task_name="place_tile", task_info=coordinate)

    def __handle_forfeit(self) -> None:
        """
        Handles forfeit action from user by queueing task
        """
        self.queue(task_name="forfeit")

    def __execute_task_place_tile(self, task_info: Tuple[int, int]) -> None:
        """
        Takes action on tile placement by communicating with model and updating view

        :param task_info: coordinate (see __handle_place_tile)
        """
        coordinate: Tuple[int, int] = task_info
        # Try placing tile. If tile placement doesn't work, don't do anything.
        # Having no action occur on a click is enough feedback to user that their click is invalid
        try:
            valid_placement = self._game.place_tile(posn=coordinate)
        except Exception:
            valid_placement = False

        # Save game if it should be saved, waiting for save to be successful with a timeout
        if self._game.save is True and valid_placement is True:
            self.__save_game()

        # If game is over, notify parent via callback
        if self._game.is_game_over():
            self.__end_game()
            return

        # Update view
        if valid_placement:
            self._view.update_game(game=self._game)
        self._view.display()
        self._game_manager.make_move()
        self._view.display()

    def __execute_task_forfeit(self) -> None:
        """
        Takes action on player forfeit by communicating with model and updating view
        """
        # Notify model who forfeited and notify parent game is over
        self._game.forfeit(self._game.curr_player)

        # Save game and end
        self.__save_game()
        self.__end_game()

    def __end_game(self) -> None:
        """
        Performs actions needed to successfully end the game
        """
        self._view.destroy()
        self._end_game_callback(self._game_manager)

    def __save_game(self):
        """
        Saves an active game in the server
        """
        try:
            server_request: SaveGameServerRequest = SaveGameServerRequest(self._game)
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
            pass
