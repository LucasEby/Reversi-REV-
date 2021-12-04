from client.controllers.base_page_controller import BasePageController
from client.controllers.end_game_page_controller import EndGamePageController
from client.controllers.play_game_page_controller import PlayGamePageController

# from client.controllers.manage_preferences_page_controller import (ManagePreferencesPageController,)
from client.controllers.pick_game_page_controller import PickGamePageController
from client.controllers.manage_preferences_page_controller import (
    ManagePreferencesPageController,
)

from client.model.game import Game
from client.model.user import User
from client.model.preference import Preference
import tkinter as tk


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        self.__window = tk.Tk()
        # self.__window.mainloop()
        self.main_user: User = User(username="P1")
        self.preferences = Preference()
        self.current_page_controller: BasePageController = PickGamePageController(
            go_home_callback=self.go_home_callback,
            play_local_callback=self.play_local_callback,
            play_online_callback=self.play_online_callback,
            manage_preferences_callback=self.manage_preferences_callback,
            main_user=self.main_user,
            window=self.__window,
        )

    def run(self) -> None:
        """
        Forever runs the active page controller
        """
        while True:
            try:
                self.current_page_controller.run()
            except:
                # print("stupid loop")
                continue

    def go_home_callback(self) -> None:
        """
        Update current page controller to welcome page when user wants to go to home screen
        """
        # This will send you to the create account page?
        pass
        # These should not be pass

    def end_game_callback(self, game: Game) -> None:
        """
        Update current page controller to end game page when gameplay has completed
        """
        self.current_page_controller: BasePageController = EndGamePageController(
            go_home_callback=self.go_home_callback,
            play_again_callback=self.play_again_callback,
            play_different_mode_callback=self.play_different_mode_callback,
            game=game,
            window=self.__window,
        )

    def play_local_callback(self, game: Game) -> None:
        """

        :param self:
        :param game:
        :return:
        """
        self.current_page_controller: BasePageController = PlayGamePageController(
            self.go_home_callback,
            self.end_game_callback,
            game,
            self.preferences,
            self.__window,
        )

    def play_online_callback(self, game: Game) -> None:
        """

        :param self:
        :param game:
        :return:
        """
        # TODO: ADD SERVER STUFF HERE
        self.current_page_controller: BasePageController = PlayGamePageController(
            self.go_home_callback,
            self.end_game_callback,
            game,
            self.preferences,
            self.__window,
        )

    def manage_preferences_callback(self) -> None:
        """
        :param self:
        :return:
        """
        self.current_page_controller: BasePageController = ManagePreferencesPageController(
                go_home_callback=self.go_home_callback,
                end_home_callback=self.end_game_callback,
                user=self.main_user
            )

    def play_again_callback(self, game: Game) -> None:
        """
        :param self:
        """
        # self.current_page_controller: BasePageController = PickGamePageController(
        #     self.go_home_callback,
        #     self.local_single_callback,
        #     self.local_multi_callback,
        #     self.online_callback,
        #     self.manage_preferences_callback,
        #     self.main_user,
        #     self.__window,
        # )
        users: tuple[User, User] = game.get_users()
        user1: User = users[0]
        user2: User = users[1]
        new_game = Game(user1, user2)
        self.current_page_controller: BasePageController = PlayGamePageController(
            end_game_callback=self.end_game_callback,
            game=new_game,
            go_home_callback=self.go_home_callback,
            preferences=self.preferences,
            window=self.__window,
        )

    def play_different_mode_callback(self):
        self.current_page_controller: BasePageController = PickGamePageController(
            go_home_callback=self.go_home_callback,
            play_local_callback=self.play_local_callback,
            play_online_callback=self.play_online_callback,
            manage_preferences_callback=self.manage_preferences_callback,
            main_user=self.main_user,
            window=self.__window,
        )


PageMachine().run()

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

# def __tile_clicked(self, row: int, col: int) -> None:
#
#     print("fish")
#     # def __display_tile_placement(self) -> None:
#     #     """
#     #     Displays graphic for user to enter tile placement info
#     #     """
#     #     valid_input: bool = False
#     #     row: int = 0
#     #     col: int = 0
#     #     print(f"\nPlayer {self._game_obj.curr_player}'s turn")
#     #     while not valid_input:
#     #         row_str: str = input("Enter row for disk: ")
#     #         col_str = input("Enter col for disk: ")
#     #         try:
#     #             row = int(row_str) - 1
#     #             col = ord(col_str.lower()) - 97
#     #         except ValueError:
#     #             print("Invalid row or col. Please try again.")
#     #             continue
#     #         valid_input = True
#     #     self._place_tile_cb((row, col))


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

# def rematch_callback(self, game: Game) -> None:
#     """
#     :param self:
#     :param game:
#     """
#     # How is this different from play again??
#     users: tuple[User, User] = game.get_users()
#     user1: User = users[0]
#     user2: User = users[1]
#     game = Game(user1, user2)
#     self.current_page_controller: BasePageController = PlayGamePageController(
#         end_game_callback=self.end_game_callback,
#         game=game,
#         go_home_callback=self.go_home_callback,
#         preferences=self.preferences,
#         window=self.__window,
#     )
