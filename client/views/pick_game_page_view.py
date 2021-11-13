from client.views.base_page_view import BasePageView
from client.controllers.pick_game_page_controller import PickGamePageController
import tkinter as tk


class PickGamePageView(BasePageView):
    def __init__(
        self,
        pgc: PickGamePageController
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.

        :param pgc: the pick game page controller object.
        """
        super().__init__()
        self._pgc = pgc

        # Set up window:
        self.__window = tk.Tk()

        # Make the main window buttons
        self.__btn_local_single_player = tk.Button(self.__window, text="Play local single player game", padx=50,
                                                   pady=50, fg="black", bg="purple",
                                                   command=self._pgc.handle_local_single_player_game())
        self.__btn_local_multiplayer_game = tk.Button(self.__window, text="Play local multiplayer game", padx=50,
                                                      pady=50, fg="black", bg="purple",
                                                      command=self._pgc.handle_local_multiplayer_game())
        self.__btn_online_game = tk.Button(self.__window, text="Play online multiplayer game", padx=50, pady=50,
                                           fg="black", bg="purple", command=self._pgc.handle_online_game())
        self.__btn_change_pref = tk.Button(self.__window, text="Change preferences", padx=50, pady=50,
                                           fg="black", bg="purple", command=self._pgc.handle_change_preferences())

        # Initialize window and button attributes:
        self.__initialize_window_and_buttons()

    def __initialize_window_and_buttons(self) -> None:
        """
        Sets the window attributes and adds the buttons to it.

        :return: None
        """
        self.__window.attributes("-topmost", 1)
        self.__window_pref.lower()

        self.__window.title("")
        self.__window_pref.title("")

        # Make it so the window is not resizable
        self.__window.resizable(False, False)
        self.__window_pref.resizable(False, False)

        # Stick the buttons on the window
        self.__btn_local_single_player.pack()
        self.__btn_local_multiplayer_game.pack()
        self.__btn_online_game.pack()

        # Start window loop
        self.__window.mainloop()

    def __destroy_buttons_and_load(self, load_message) -> None:
        """
        Destroys the buttons and displays the loading screen.

        :param self: the PickGamePageView object.
        :param load_message: the load message that is displayed to the user
        :return: None
        """
        self.__btn_local_single_player.destroy()
        self.__btn_local_multiplayer_game.destroy()
        self.__btn_online_game.destroy()
        L = tk.Label(self.__window, text=load_message)
        L.pack()

    def display_matchmaking_load_local_single(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading local single player game...")
        self._pgc.handle_local_single_player_game()

    def display_matchmaking_load_local_multi(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading local multi player game...")
        self._pgc.handle_local_multiplayer_game()

    def display_matchmaking_load_online(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading online multi player game...")
        self._pgc.handle_online_game()
