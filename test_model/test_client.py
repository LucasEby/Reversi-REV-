import unittest
from _thread import *

from client.client_comm_manager import ClientCommManager
from client.credential_check_request import CredentialCheckRequest


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.comm: ClientCommManager = ClientCommManager()

    def test_client_manager_singleton(self) -> None:
        """
        This test makes sure that the singleton is working so that error message will be given if the class is
        constructed more than once.
        """
        with self.assertRaises(Exception) as context:
            ClientCommManager()
        self.assertTrue("This class is a singleton!" in str(context.exception))

    def test_run_client(self) -> None:
        """
        This test method represents a main program that starts a client side connection to check the login information.
        """
        while True:
            username: str = input("Enter your username: ")
            password: str = input("Enter your password: ")
            if username == "q" or password == "q":
                self.comm.close_the_connection()
                break
            login = CredentialCheckRequest()
            login.send_login(username, password)
            start_new_thread(self.comm.run, ())
            # login.check_credential_check_request()
        # comm.send_game_match_request(777)


if __name__ == "__main__":
    unittest.main()
