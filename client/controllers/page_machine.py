from client.controllers.base_page_controller import BasePageController
from client.controllers.play_game_page_controller import PlayGamePageController
from client.model.game import Game
from client.model.user import User
from client.model.game_manager import GameManager
from client.model.player import Player


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        main_user: User = User(username="P1")
        main_user.get_preference().set_board_size(8)
        player1 = Player(2)
        player2 = Player(1)
        game_manager = GameManager(player1=player1, player2=player2,
                                   board_size=main_user.get_preference().get_board_size(),
                                   rules=main_user.get_preference().get_rule())
        self.current_page_controller: BasePageController = PlayGamePageController(
            go_home_callback=self.go_home_callback,
            end_game_callback=self.end_game_callback,
            game_manager=game_manager,
            main_user=main_user
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
        pass

    def end_game_callback(self, game_manager: GameManager) -> None:
        """
        Update current page controller to end game page when gameplay has completed
        """
        pass
