from client.views.base_page_view import BasePageView
import tkinter as tk
from typing import Callable


class PickGamePageView(BasePageView):
    def __init__(
        self,
        local_single_callback: Callable[[], None],
        local_multi_callback: Callable[[], None],
        online_callback: Callable[[], None],
        change_preferences_callback: Callable[[], None],
        window,
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.
        """
        super().__init__(window=window)
        self._local_single_callback = local_single_callback
        self._local_multi_callback = local_multi_callback
        self._online_callback = online_callback
        self._change_preferences_callback = change_preferences_callback
        # self._window = window
        # Make the main window buttons
        self.__btn_local_single_player = tk.Button(
            self._frame,
            text="Play local single player game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self._local_single_callback,
        )
        self.__btn_local_multiplayer_game = tk.Button(
            self._frame,
            text="Play local multiplayer game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self._local_multi_callback,
        )
        self.__btn_online_game = tk.Button(
            self._frame,
            text="Play online multiplayer game",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self._online_callback,
        )
        self.__btn_change_pref = tk.Button(
            self._frame,
            text="Change preferences",
            padx=50,
            pady=50,
            fg="black",
            bg="purple",
            command=self._change_preferences_callback,
        )

    def display(self) -> None:
        """
        Sets the window attributes and adds the buttons to it.

        :return: None
        """
        # Stick the buttons on the window
        self.__btn_local_single_player.pack()
        self.__btn_local_multiplayer_game.pack()
        self.__btn_online_game.pack()
        self.__btn_change_pref.pack()
        self._frame.lift()
        # Start window loop
        self._frame.mainloop()

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
        self.__btn_change_pref.destroy()
        L = tk.Label(self._frame, text=load_message)
        L.pack()

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
