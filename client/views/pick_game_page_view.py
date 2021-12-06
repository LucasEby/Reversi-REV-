from client.views.home_button_page_view import HomeButtonPageView
import tkinter as tk
from typing import Callable, Any


class PickGamePageView(HomeButtonPageView):
    def __init__(
        self,
        local_single_callback: Callable[[], None],
        local_multi_callback: Callable[[], None],
        online_callback: Callable[[], None],
        change_preferences_callback: Callable[[], None],
        go_home_callback: Callable[[], None],
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.
        """
        super().__init__(go_home_callback=go_home_callback)
        self._local_single_callback: Callable[[], None] = local_single_callback
        self._local_multi_callback: Callable[[], None] = local_multi_callback
        self._online_callback: Callable[[], None] = online_callback
        self._change_preferences_callback: Callable[
            [], None
        ] = change_preferences_callback
        self.__btn_local_single_player: tk.Button = self.__create_pick_game_button(
            label="Play local single player game", command=self._local_single_callback
        )
        self.__btn_local_multiplayer_game: tk.Button = self.__create_pick_game_button(
            label="Play local multiplayer game", command=self._local_multi_callback
        )
        self.__btn_online_game: tk.Button = self.__create_pick_game_button(
            label="Play online multiplayer game", command=self._online_callback
        )
        self.__btn_change_pref: tk.Button = self.__create_pick_game_button(
            label="Manage Preferences", command=self._change_preferences_callback
        )
        self.display()

    def __create_pick_game_button(
        self, label: str, command: Callable[..., Any]
    ) -> tk.Button:
        """
        Creates a generic button for picking the game
        :param label: What text should be on the button
        :param command: What calback should be attached to the button press
        :return Generated button
        """
        return tk.Button(
            self._frame,
            text=label,
            padx=20,
            pady=20,
            fg="black",
            bg="green",
            command=command,
        )

    def display(self) -> None:
        """
        Sets the window attributes and adds the buttons to it.
        """
        super().display()
        # Stick the buttons on the window
        self.__btn_local_single_player.pack()
        self.__btn_local_multiplayer_game.pack()
        self.__btn_online_game.pack()
        self.__btn_change_pref.pack()

    def destroy(self) -> None:
        """
        Destroys the buttons
        """
        super().destroy()
        self.__btn_local_single_player.destroy()
        self.__btn_local_multiplayer_game.destroy()
        self.__btn_online_game.destroy()
        self.__btn_change_pref.destroy()
