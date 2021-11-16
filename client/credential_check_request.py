from _thread import start_new_thread
from typing import Dict

from client.client_comm_manager import ClientCommManager


class CredentialCheckRequest:
    def __init__(self) -> None:
        # get the constructed ClientCommManager
        self.client_manager = ClientCommManager.get_instance()

    def send_login(self, username: str, password: str) -> None:
        """
        Prepare the login information to be sent to the server.

        :param username: username string typed in by the user
        :param password: password string typed in by the user
        """
        data = {
            "protocol_type": "client_login",
            "username": username,
            "password": password,
        }
        self.client_manager.send(data, self.print_method_to_test)

    def print_method_to_test(self, success: bool, protocol: Dict[str, str]) -> None:
        """
        This is just a method representing the callable passed in with login message for testing.
        """
        print("This is a method only for testing if CALLABLE functions well.")
        print("Message transfer status: " + str(success))
        print("username: " + protocol["username"])
        print("password: " + protocol["password"])
