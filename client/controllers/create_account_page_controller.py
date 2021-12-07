from typing import Callable

from client.controllers.base_page_controller import BasePageController
from client.controllers.home_button_page_controller import HomeButtonPageController
from client.views.create_account_page_view import CreateAccountPageView
from client.model.user import User


class CreateAccountPageController(HomeButtonPageController):
    def __init__(
        self,
        go_home_callback: Callable[[], None],
        login_callback: Callable[[User], None],
    ) -> None:
        """
        Page controller to handle creating a new user

        :param go_home_callback: Callback to call when going to the home screen
        :param login_callback: Callback to handle creating a new account
        """
        super().__init__()

        self.__go_home_callback: Callable[[], None] = go_home_callback
        self.__login_callback: Callable[[User], None] = login_callback

        self._task_execute_dict["login_button"] = self.__execute_task_login_button
        self.__view = CreateAccountPageView(
            self,
            go_home_cb=self.__handle_home_button,
            login_cb=self.__handle_login_button,
        )

    def __handle_login_button(self, Uname, Pword) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="login_button", task_info=(Uname, Pword))

    def __execute_task_login_button(self, next_task_info) -> None:
        """
        Notifies upper level to create a new account and login that account
        """
        Uname, Pword = next_task_info
        # ADD SERVER COMM FOR MAKING NEW USER
        self.__login_callback()
        self.__view.destroy()
