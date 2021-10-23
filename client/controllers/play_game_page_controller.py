from client.controllers.home_button_page_controller import HomeButtonPageController


class PlayGamePageController(HomeButtonPageController):
    def __init__(self):
        """
        Page controller used for handling and responding to user inputs that occur in-game
        """
        super().__init__()
