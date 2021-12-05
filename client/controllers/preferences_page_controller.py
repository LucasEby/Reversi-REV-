from typing import Callable

from client.controllers.base_page_controller import BasePageController
from client.views.preferences_page_view import PreferencesPageView


class PreferencesPageController(BasePageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        # TODO: add callbacks
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
        # TODO: add callbacks

        self._frame = frame

        self._task_execute_dict["submit_button"] = self.__execute_task_submit_button

        self.__view = PreferencesPageView(
            self,
            self.__go_home_callback,
            # TODO: add callbacks
            self._frame,
        )

    # TODO: add callbacks
    def __handle_submit_button(self) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="submit_button")

    def __execute_task_submit_button(self) -> None:
        # TODO: add callbacks
        pass
