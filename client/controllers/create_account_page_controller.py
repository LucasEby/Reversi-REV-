from typing import Callable

from client.controllers.base_page_controller import BasePageController
from client.views.create_account_page_view import CreateAccountPageView


class CreateAccountPageController(BasePageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
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

        self._frame = frame

        self._task_execute_dict["login_button"] = self.__execute_task_login_button

        self.__view = CreateAccountPageView(
            self,
            self.__go_home_callback,
            self._frame,
        )

    def __handle_login_button(self) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="login_button")

    def __execute_task_login_button(self) -> None:
        self._login_callback()
