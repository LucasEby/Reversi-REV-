from typing import Callable

from client.controllers.base_page_controller import BasePageController
from client.views.welcome_page_view import WelcomePageView


class WelcomePageController(BasePageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        login_callback: Callable[[], None],
        create_account_callback: Callable[[], None],
        play_as_guest_callback: Callable[[], None],
        frame,
    ) -> None:
        """
        TODO: add proper comments
        Specific type of page controller with a home button already handled.
        Many pages could have a home button, so this removes duplicate code.
        :param go_home_callback: Callback to call when going to the home screen
        """
        super().__init__()

        self.__go_home_callback: Callable[[], None] = go_home_callback
        self._login_callback: Callable[[], None] = login_callback
        self._create_account_callback: Callable[[], None] = create_account_callback
        self._play_as_guest_callback: Callable[[], None] = play_as_guest_callback
        self._frame = frame

        self._task_execute_dict["login_button"] = self.__execute_task_login_button
        self._task_execute_dict[
            "create_account_button"
        ] = self.__execute_task_create_account_button
        self._task_execute_dict[
            "play_as_guest_button"
        ] = self.__execute_task_play_as_guest_button

        self.__view = WelcomePageView(
            self,
            self.__go_home_callback,
            self._login_callback,
            self._create_account_callback,
            self._play_as_guest_callback,
            self._frame,
        )

    def __handle_login_button(self) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="login_button")

    def __execute_task_login_button(self) -> None:
        self._login_callback()

    def __handle_create_account_button(self) -> None:
        """
        Handles create account button action from the user by queueing task
        """
        self.queue(task_name="create_account_button")

    def __execute_task_create_account_button(self) -> None:
        self._create_account_callback()

    def __handle_play_as_guest_button(self) -> None:
        """
        Handles "Play as Guest" button action from the user by queueing task
        """
        self.queue(task_name="play_as_guest_button")

    def __execute_task_play_as_guest_button(self) -> None:
        self._play_as_guest_callback()
