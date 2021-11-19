from client.views.base_page_view import BasePageView
import tkinter as tk

try:
    from client.controllers.pick_game_page_controller import PickGamePageController
except ImportError:
    import sys

    PickGamePageController = sys.modules["client.controllers.pick_game_page_controller"]
    # __package__ + '.PickGamePageController']


class PickGamePageView(BasePageView):
    def __init__(self, pgc: PickGamePageController, window) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.

        :param pgc: the pick game page controller object.
        """
        super().__init__(window=window)
        self.__pgc = pgc

        # Make the main window buttons
        self.__btn_local_single_player = tk.Button(
            self._frame,
            text="Play local single player game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self.__local_single_clicked,
        )
        self.__btn_local_multiplayer_game = tk.Button(
            self._frame,
            text="Play local multiplayer game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self.__local_multi_clicked,
        )
        self.__btn_online_game = tk.Button(
            self._frame,
            text="Play online multiplayer game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self.__online_clicked,
        )
        self.__btn_change_pref = tk.Button(
            self._frame,
            text="Change preferences",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=pgc.handle_change_preferences,
        )

    def start_gui(self) -> None:
        """
        Sets the window attributes and adds the buttons to it.

        :return: None
        """
        # Stick the buttons on the window
        self.__btn_local_single_player.pack()
        self.__btn_local_multiplayer_game.pack()
        self.__btn_online_game.pack()

        # self._frame.attributes("-topmost", 1)
        self._frame.lift()

        # Start window loop
        # self._frame.mainloop()

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
        L = tk.Label(self._frame, text=load_message)
        L.pack()

    def __local_single_clicked(self) -> None:
        self.__pgc.handle_local_single_player_game()

    def __local_multi_clicked(self) -> None:
        self.__pgc.handle_local_multiplayer_game()

    def __online_clicked(self) -> None:
        self.__pgc.handle_online_game()

    def display_local_single_player_game_chosen(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading local single player game...")

    def display_local_multiplayer_game_chosen(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading local multi player game...")

    def display_online_game_chosen(self) -> None:
        """
        Displays "loading local single player game" and calls the local single player game handle in the
        controller.

        :param self: the PickGamePageView object.
        :return: None
        """
        self.__destroy_buttons_and_load("Loading online multi player game...")
