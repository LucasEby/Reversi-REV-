from client.client_comm_manager import ClientCommManager


class CredentialCheckRequest:
    def __init__(self, client_manager: ClientCommManager) -> None:
        self.client_manager = client_manager

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
        self.client_manager.send(data)

    def check_credential_check_request(self) -> bool:
        """
        Check the result from the server.
        TODO: Expected server returned message contains:
            - match or not ?
            - user id ?
        :returns: True if the username and password pair matches one in the database; otherwise return False
        """
        result = self.client_manager.get_returned_message("username")
        print(result)  # TODO: replaced by checking credential result
        # if result_message == 'correct':
        #     return True
        return False
