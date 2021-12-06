from client.controllers.base_page_controller import BasePageController
from client.controllers.end_game_page_controller import EndGamePageController
from client.controllers.play_game_page_controller import PlayGamePageController
from client.controllers.pick_game_page_controller import PickGamePageController
from client.controllers.manage_preferences_page_controller import (
    ManagePreferencesPageController,
)
from client.model.game_manager import GameManager
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

    def end_game_callback(self, game_manager: GameManager) -> None:
        """
        Update current page controller to end game page when gameplay has completed

        :param game_manager: Contains the main user of the application and Game once it was completed
        """
        self.current_page_controller = EndGamePageController(
            go_home_callback=self.go_home_callback,
            play_again_callback=self.play_again_callback,
            play_different_mode_callback=self.play_different_mode_callback,
            game_manager=game_manager
        )

    def game_picked_callback(self, game_manager: GameManager) -> None:
        """
        Starts playing game once one has been created

        :param game_manager: Contains the main user of the application and the picked game
        """
        self.current_page_controller = PlayGamePageController(
            end_game_callback=self.end_game_callback,
            game_manager=game_manager
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

    def play_again_callback(self, game_manager: GameManager) -> None:
        """
        Plays game again with a created game

        :param game_manager: Contains the main user of the application and the game to play with
        """
        self.current_page_controller = PlayGamePageController(
            end_game_callback=self.end_game_callback,
            game_manager=game_manager
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
