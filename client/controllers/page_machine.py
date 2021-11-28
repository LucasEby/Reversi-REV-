from client.controllers.base_page_controller import BasePageController
from client.controllers.play_game_page_controller import PlayGamePageController
from client.controllers.manage_preferences_page_controller import (
    ManagePreferencesPageController,
)
from client.controllers.pick_game_page_controller import PickGamePageController
from client.views.pick_game_page_view import PickGamePageView

from client.model.game import Game
from client.model.user import User
import tkinter as tk


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        self.__window = tk.Tk()
        # self.__window.mainloop()
        self.main_user: User = User(id_num=1, username="P1")
        self.current_page_controller: BasePageController = PickGamePageController(
            go_home_callback=self.go_home_callback,
            local_single_callback=self.local_single_callback,
            local_multi_callback=self.local_multi_callback,
            online_callback=self.online_callback,
            manage_preferences_callback=self.manage_preferences_callback,
            main_user=self.main_user,
            window=self.__window,
        )
        self.run()

    def run(self) -> None:
        """
        Forever runs the active page controller
        """
        while True:
            self.current_page_controller.run()

    def go_home_callback(self) -> None:
        """
        Update current page controller to welcome page when user wants to go to home screen
        """
        pass
        # These should not be pass

    def end_game_callback(self, game: Game) -> None:
        """
        Update current page controller to end game page when gameplay has completed
        """
        # TODO:
        # self.current_page_controller =
        # These should not be pass
        self.current_page_controller = EndGamePageController(
            self,
            self.go_home_callback,
            self.rematch_callback,
            self.play_again_callback,
            game,
            self.__window,
        )

    def local_single_callback(self, game: Game) -> None:
        """
        :param self:
        :param game:
        :return:
        """
        # print("play local single player game")
        self.current_page_controller = PlayGamePageController(
            self.go_home_callback, self.end_game_callback, game
        )
        # These should not be pass

    def local_multi_callback(self, game: Game) -> None:
        """

        :param self:
        :param game:
        :return:
        """
        self.current_page_controller = PlayGamePageController(
            self.go_home_callback, self.end_game_callback, game
        )

    def online_callback(self, game: Game) -> None:
        """

        :param self:
        :param game:
        :return:
        """
        self.current_page_controller = PlayGamePageController(
            self.go_home_callback, self.end_game_callback, game
        )
        # self.current_page_controller = PlayGamePageController(self.go_home_callback, self.end_game_callback, game)
        # These should not be pass

    def manage_preferences_callback(self, game: Game) -> None:
        """

        :param self:
        :param game:
        :return:
        """
        # self.current_page_controller = ManagePreferencesPageController(self.go_home_callback,
        # self.end_game_callback, User(id_num=1, username="P1"))
        pass
        # These should not be pass
    def play_again_callback(self) -> None:
        """
        :param self:
        """
        self.current_page_controller = PickGamePageController(
            self.go_home_callback,
            self.local_single_callback,
            self.local_multi_callback,
            self.online_callback,
            self.manage_preferences_callback,
            self.main_user,
            self.__window,
        )

    def rematch_callback(self) -> None:
        """
        :param self:
        """
        # TODO: Need actual rematch capabilites

        # self.current_page_controller = PickGamePageController()


PageMachine()

# main_user.get_preference().set_board_size(4)
# main_user: User = User(id_num=1, username="P1")
# main_user.get_preference().set_board_size(4)
# self.current_page_controller: BasePageController = PlayGamePageController(
#     go_home_callback=self.go_home_callback,
#     end_game_callback=self.end_game_callback,
#     game=Game(
#         user1=User(id_num=2, username="P2"),
#         user2=main_user,
#         p1_first_move=False,
#     ),
# )
# self.current_page_controller = PickGamePageView(PickGamePageController(
#     go_home_callback=self.go_home_callback,
#     play_local_single_player_game_callback=self.play_local_single_player_game_callback,
#     play_local_multiplayer_game_callback=self.play_local_multiplayer_game_callback,
#     play_online_game_callback=self.play_online_game_callback,
#     manage_preferences_callback=self.manage_preferences_callback
# )
# )
# self.current_page_controller = PickGamePageController(PickGamePageView())

# go_home_callback: Callable[[], None],
# play_local_single_player_game_callback: Callable[[Game], None],
# play_local_multiplayer_game_callback: Callable[[Game], None],
# play_online_game_callback: Callable[[Game], None],
# manage_preferences_callback: Callable[[Game], None],
# self.current_page_controller: BasePageController =
