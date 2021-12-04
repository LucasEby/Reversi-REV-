from typing import Tuple, Callable, List

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.game import Game
from client.model.preference import Preference
from client.views.play_game_page_view import PlayGamePageView


class PlayGamePageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        end_game_callback: Callable[[Game], None],
        game: Game,
        preferences: Preference,
        window,
    ) -> None:
        """
        Page controller used for handling and responding to user inputs that occur in-game
        :param go_home_callback: Callback to call when user requested going to the home screen
        :param end_game_callback: Callback to call after a game ended
        :param game: Game that was created to play the game with
        """
        super().__init__(go_home_callback=go_home_callback, window=window)
        self._task_execute_dict["place_tile"] = self.__execute_task_place_tile
        self._task_execute_dict["forfeit"] = self.__execute_task_forfeit
        self._task_execute_dict["end_game"] = self.__execute_end_game

        self._end_game_callback: Callable[[Game], None] = end_game_callback
        self._game = game
        self.__view = PlayGamePageView(
            game=self._game,
            place_tile_cb=self.__handle_place_tile,
            forfeit_cb=self.__handle_forfeit,
            preferences=preferences,
            end_game_callback=self.__execute_end_game,
            go_home_callback=go_home_callback,
            window=window,
        )

    def __handle_place_tile(self, coordinate: tuple[int, int]) -> None:
        """
        Handles tile placement action from the user by queueing task
        :param coordinate: Coordinate on board (down, right) where tile placement was attempted
        """
        if not self._game.is_game_over():
            valid_moves: List[List[bool]] = self._game.get_valid_moves()
            if self._game.board.is_valid_posn(coordinate[0], coordinate[1]):
                if valid_moves[coordinate[0]][coordinate[1]]:
                    self.__execute_task_place_tile(coordinate)
        else:
            self.queue(task_name="end_game", task_info=None)
            # self._end_game_callback(self._game)
            self.__view.execute_end_game()

    def __handle_forfeit(self, player_num: int) -> None:
        """
        Handles forfeit action from user by queueing task
        :param player_num: Player number who forfeited
        """
        self.queue(task_name="forfeit", task_info=player_num)
        self.__execute_task_forfeit(player_num)

    def __execute_task_place_tile(self, task_info: Tuple[int, int]) -> None:
        """
        Takes action on tile placement by communicating with model and updating view
        :param task_info: coordinate (see __handle_place_tile)
        """
        self._game.place_tile(task_info)
        self.__view.display()
        if self._game.is_game_over():
            self.queue(task_name="end_game", task_info=None)
            self.__view.execute_end_game()

    def __execute_task_forfeit(self, task_info: int) -> None:
        """
        Takes action on player forfeit by communicating with model and updating view
        :param task_info: player_num (see __handle_forfeit)
        """
        player_num = task_info
        self.__view.display_player_forfeit(player_num)
        # Notify model who forfeited and notify parent game is over
        self._game.forfeit(self._game.curr_player)
        self.__execute_end_game()

    def __execute_end_game(self):
        self._end_game_callback(self._game)

    def run(self):
        self.__view.display()


# def run(self):
#     self.__view.start_gui()


# play game controller calls end game callback
# in page machine:
# self.currentPageController.run()
#
# play game page view in the main branch
# instead of calling playgamecontroller.callback


# def place_tile_callback(self, coordinate: Tuple[int, int]):
#     valid_input: bool = False
#     row: int = 0
#     col: int = 0
#     print(f"\nPlayer {self._game_obj.curr_player}'s turn")
#     while not valid_input:
#         row_str: str = input("Enter row for disk: ")
#         col_str = input("Enter col for disk: ")
#         try:
#             row = int(row_str) - 1
#             col = ord(col_str.lower()) - 97
#         except ValueError:
#             print("Invalid row or col. Please try again.")
#             continue
#         valid_input = True
#     self._place_tile_cb((row, col))
