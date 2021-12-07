from client.controllers.base_page_controller import BasePageController
from client.controllers.end_game_page_controller import EndGamePageController
from client.controllers.play_game_page_controller import PlayGamePageController
from client.controllers.pick_game_page_controller import PickGamePageController
from client.controllers.manage_preferences_page_controller import (
    ManagePreferencesPageController,
)

from client.model.game import Game
from client.model.user import User


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        main_user: User = User(username="P1")
        self.current_page_controller: BasePageController = PickGamePageController(
            go_home_callback=self.go_home_callback,
            game_picked_callback=self.game_picked_callback,
            manage_preferences_callback=self.manage_preferences_callback,
            main_user=main_user,
        )

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
        # This will send you to the welcome page
        pass

    def end_game_callback(self, game: Game, main_user: User) -> None:
        """
        Update current page controller to end game page when gameplay has completed

        :param game: Game once it was completed
        :param main_user: Main user of the application
        """
        self.current_page_controller = EndGamePageController(
            go_home_callback=self.go_home_callback,
            play_again_callback=self.play_again_callback,
            play_different_mode_callback=self.play_different_mode_callback,
            game=game,
            main_user=main_user,
        )

    def game_picked_callback(self, game: Game, main_user: User) -> None:
        """
        Starts playing game once one has been created

        :param game: Game that was created
        :param main_user: Primary user in the application
        """
        self.current_page_controller = PlayGamePageController(
            end_game_callback=self.end_game_callback,
            game=game,
            main_user=main_user,
        )

    def manage_preferences_callback(self, user: User) -> None:
        """
        Goes to manage preferences page

        :param user: User whose preferences should be changed
        """
        self.current_page_controller = ManagePreferencesPageController(
            go_home_callback=self.go_home_callback,
            preferences_complete_callback=self.go_home_callback,
            user=user,
        )

    def play_again_callback(self, game: Game, main_user: User) -> None:
        """
        Plays game again with a created game

        :param game: Game to play again with
        :param main_user: Primary user in the application
        """
        self.current_page_controller = PlayGamePageController(
            end_game_callback=self.end_game_callback,
            game=game,
            main_user=main_user,
        )

    def play_different_mode_callback(self, main_user: User):
        """
        Goes to play a different game mode

        :param main_user: Main user in the application
        """
        self.current_page_controller = PickGamePageController(
            go_home_callback=self.go_home_callback,
            game_picked_callback=self.game_picked_callback,
            manage_preferences_callback=self.manage_preferences_callback,
            main_user=main_user,
        )

    def change_preferences_callback(self):
