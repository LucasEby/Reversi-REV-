from client.controllers.base_page_controller import BasePageController
from client.controllers.play_game_page_controller import PlayGamePageController
from client.model.game import Game
from client.model.user import User


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        main_user: User = User(id_num=1, username="P1")
        main_user.get_preference().set_board_size(8)
        self.current_page_controller: BasePageController = PlayGamePageController(
            go_home_callback=self.go_home_callback,
            end_game_callback=self.end_game_callback,
            game=Game(
                user1=User(id_num=2, username="P2"),
                user2=main_user,
                p1_first_move=False,
                save=True,
            ),
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

    def end_game_callback(self, game: Game) -> None:
        """
        Update current page controller to end game page when gameplay has completed
        """
        pass
