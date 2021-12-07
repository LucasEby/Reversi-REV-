from client.views.home_button_page_view import HomeButtonPageView
import tkinter as tk
from typing import Callable, Any, Optional


class PickGamePageView(HomeButtonPageView):
    def __init__(
        self,
        local_single_callback: Callable[[], None],
        local_multi_callback: Callable[[], None],
        online_callback: Callable[[], None],
        change_preferences_callback: Callable[[], None],
        go_home_callback: Callable[[], None],
        username: str,
        resume_game_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Creates the button window with the 3 buttons: a local single player button, a local multiplayer button,
        and an online multiplayer button. When a button is clicked, a "loading game" message is displayed and the
        controller is notified.

        :param local_single_callback: Single player vs AI local game button cb
        :param local_multi_callback: Multiplayer local game button cb
        :param online_callback: Online game cb
        :param change_preferences_callback: Change preferences button cb
        :param go_home_callback: Go home button cb
        :param username: Username of main user
        :param resume_game_callback: Resume game button callback, or None if there shouldn't be a resume game button
        """
        super().__init__(go_home_callback=go_home_callback)
        self._local_single_callback: Callable[[], None] = local_single_callback
        self._local_multi_callback: Callable[[], None] = local_multi_callback
        self._online_callback: Callable[[], None] = online_callback
        self._change_preferences_callback: Callable[
            [], None
        ] = change_preferences_callback
        self._resume_game_callback: Optional[Callable[[], None]] = resume_game_callback
        self._label_welcome: tk.Label = tk.Label(
            self._frame, text=f"Hi, {username}!", font=("Arial", 18)
        )
        self._btn_local_single_player: tk.Button = self.__create_pick_game_button(
            label="Play local single player game", command=self._local_single_callback
        )
        self._btn_local_multiplayer_game: tk.Button = self.__create_pick_game_button(
            label="Play local multiplayer game", command=self._local_multi_callback
        )
        self._btn_online_game: tk.Button = self.__create_pick_game_button(
            label="Play online multiplayer game", command=self._online_callback
        )
        self._btn_change_pref: tk.Button = self.__create_pick_game_button(
            label="Manage Preferences", command=self._change_preferences_callback
        )
        if self._resume_game_callback is not None:
            self._btn_resume_game: tk.Button = self.__create_pick_game_button(
                label="Resume Previous Game", command=self._resume_game_callback
            )
        self.display()

    def __create_pick_game_button(
        self, label: str, command: Callable[..., Any]
    ) -> tk.Button:
        """
        Creates a generic button for picking the game
        :param label: What text should be on the button
        :param command: What callback should be attached to the button press
        :return Generated button
        """
        return tk.Button(
            self._frame,
            text=label,
            padx=20,
            pady=20,
            fg="white",
            bg="green",
            command=command,
        )

    def display(self) -> None:
        """
        Sets the window attributes and adds the buttons to it.
        """
        super().display()
        # Stick the buttons on the window
        self._label_welcome.pack()
        self._btn_local_single_player.pack(fill="x")
        self._btn_local_multiplayer_game.pack(fill="x")
        self._btn_online_game.pack(fill="x")
        self._btn_change_pref.pack(fill="x")
        if self._resume_game_callback is not None:
            self._btn_resume_game.pack(fill="x")

    def destroy(self) -> None:
        """
        Destroys the buttons
        """
        super().destroy()
        self._label_welcome.destroy()
        self._btn_local_single_player.destroy()
        self._btn_local_multiplayer_game.destroy()
        self._btn_online_game.destroy()
        self._btn_change_pref.destroy()
