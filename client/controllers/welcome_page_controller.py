import time
from typing import Callable, Tuple, List, Optional

from random_word import RandomWords  # type: ignore

from client.controllers.base_page_controller import BasePageController
from client.model.account import Account
from client.model.calculate_new_elos import CalculateNewELOs
from client.model.password_crypter import PasswordCrypter
from client.model.user import User
from client.server_comms.credential_check_server_request import (
    CredentialCheckServerRequest,
)
from client.server_comms.get_top_elos_server_request import GetTopELOsServerRequest
from client.views.welcome_page_view import WelcomePageView


class WelcomePageController(BasePageController):

    _CREDENTIAL_CHECK_TIMEOUT_SEC: float = 5

    def __init__(
        self,
        user_created_callback: Callable[[User], None],
        create_account_callback: Callable[[], None],
    ) -> None:
        """
        Page controller for welcoming the user and letting them choose how to proceed
        """
        super().__init__()

        self._user_created_callback: Callable[[User], None] = user_created_callback
        self._create_account_callback: Callable[[], None] = create_account_callback

        self._task_execute_dict["login"] = self.__execute_task_login
        self._task_execute_dict["create_account"] = self.__execute_task_create_account
        self._task_execute_dict["play_as_guest"] = self.__execute_task_play_as_guest

        elos: List[Tuple[str, int]] = self.__retrieve_elos()
        self._view = WelcomePageView(
            self.__handle_login,
            self.__handle_create_account,
            self.__handle_play_as_guest,
            elos,
        )

    @staticmethod
    def __retrieve_elos() -> List[Tuple[str, int]]:
        """
        Get ELOS from server

        :return List of ELOs
        """
        server_request: GetTopELOsServerRequest = GetTopELOsServerRequest(num_elos=10)
        server_request.send()
        # Wait for request to finish
        start_time = time.time()
        while server_request.is_response_success() is None:
            if time.time() - start_time > 5:
                break
        elos: Optional[List[Tuple[str, int]]] = server_request.get_top_elos()
        if elos is None:
            return []
        return elos

    def __handle_login(self, username: str, password: str) -> None:
        """
        Handles login button action from the user by queueing task
        """
        self.queue(task_name="login", task_info=(username, password))

    def __handle_create_account(self) -> None:
        """
        Handles create account button action from the user by queueing task
        """
        self.queue(task_name="create_account")

    def __handle_play_as_guest(self) -> None:
        """
        Handles "Play as Guest" button action from the user by queueing task
        """
        self.queue(task_name="play_as_guest")

    def __execute_task_login(self, task_info: Tuple[str, str]) -> None:
        """
        Check credentials from entries. Notify GUI if wrong or login if correct
        """
        # Get user info
        username: str
        entered_password: str
        username, entered_password = task_info

        # Get credentials from server
        account: Optional[Account] = None
        encrypted_password: Optional[str] = None
        try:
            server_request: CredentialCheckServerRequest = CredentialCheckServerRequest(
                username=username
            )
            server_request.send()
            start_time: float = time.time()
            while server_request.is_response_success() is None:
                if time.time() - start_time > self._CREDENTIAL_CHECK_TIMEOUT_SEC:
                    raise ConnectionError(
                        "Server unresponsive. Account could not be created"
                    )
            if server_request.is_response_success() is False:
                raise ConnectionError("Server could not properly create account")
            else:
                encrypted_password = server_request.get_encrypted_password()
                account = server_request.get_account()
        except ConnectionError as e:
            # TODO: Notify view of server error
            print(e)

        # Check passwords match
        password_correct: bool = False
        if encrypted_password is not None and account is not None:
            password_correct = entered_password == encrypted_password
            # password_correct = PasswordCrypter.is_match(
            #    entered_password, encrypted_password.encode("utf-8")
            # )

        # If passwords match, create account
        if password_correct and account is not None:
            self._view.destroy()
            self._user_created_callback(account)

    def __execute_task_create_account(self) -> None:
        """
        Notify upper level when create account requested
        """
        self._view.destroy()
        self._create_account_callback()

    def __execute_task_play_as_guest(self) -> None:
        """
        Creates a guest to play as before notifying upper level
        """
        rand_word: str = RandomWords().get_random_word()
        new_user: User = User(username=f"Guest {rand_word.capitalize()}")
        self._view.destroy()
        self._user_created_callback(new_user)
