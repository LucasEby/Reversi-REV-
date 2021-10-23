from client.controllers.base_page_controller import BasePageController
from client.controllers.play_game_page_controller import PlayGamePageController


class PageMachine:
    def __init__(self) -> None:
        """
        Class that controls which page controller is currently active.
        Based on callbacks from the various page controllers, the next page controller can be determined.
        """
        self.current_page_controller: BasePageController = PlayGamePageController()

    def run(self) -> None:
        """
        Forever runs the active page controller
        """
        while True:
            self.current_page_controller.run()
