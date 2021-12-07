from typing import Callable
import time

from client.controllers.home_button_page_controller import HomeButtonPageController
from client.model.account import Account
from client.model.calculate_new_elos import CalculateNewELOs
from client.model.password_crypter import PasswordCrypter
from client.server_comms.create_account_server_request import CreateAccountServerRequest
from client.views.create_account_page_view import CreateAccountPageView
from client.model.user import User


class CreateAccountPageController(HomeButtonPageController):

    _CREATE_ACCOUNT_TIMEOUT_SEC: float = 5

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
        super().__init__(go_home_callback=go_home_callback)

        self.__login_callback: Callable[[User], None] = login_callback

        self._task_execute_dict["login_button"] = self.__execute_task_login_button
        self.__view = CreateAccountPageView(
            go_home_cb=self.handle_home_button,
            login_cb=self.__handle_login_button,
        )

    def __handle_login_button(self, u_name: str, p_word: str) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="login_button", task_info=(u_name, p_word))

    def __execute_task_login_button(self, next_task_info) -> None:
        """
        Notifies upper level to create a new account and login that account
        """
        username, password = next_task_info
        account: Account = Account(
            username=username, elo=CalculateNewELOs.DEFAULT_ELO, account_id=0
        )

        # Encrypt password
        # encrypted_password: bytes = PasswordCrypter.encrypt(password=password)
        encrypted_password: bytes = password.encode("utf-8")
        string_password: str = "".join(map(chr, encrypted_password))

        try:
            server_request: CreateAccountServerRequest = CreateAccountServerRequest(
                account, string_password
            )
            server_request.send()
            start_time: float = time.time()
            while server_request.is_response_success() is None:
                if time.time() - start_time > self._CREATE_ACCOUNT_TIMEOUT_SEC:
                    raise ConnectionError(
                        "Server unresponsive. Account could not be created"
                    )
            if server_request.is_response_success() is False:
                raise ConnectionError("Server could not properly create account")
            else:
                account = Account(
                    username,
                    CalculateNewELOs.DEFAULT_ELO,
                    server_request.get_account_id(),
                )
        except ConnectionError as e:
            # TODO: Notify view of server error
            print(e)

        self.__login_callback(account)
        self.__view.destroy()
