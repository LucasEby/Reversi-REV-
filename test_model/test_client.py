import threading
import unittest
from _thread import *

from client.client_comm.client_comm_manager import ClientCommManager
from client.client_comm.credential_check_request import CredentialCheckRequest


class MyTestCase(unittest.TestCase):
    comm = None

    @classmethod
    def setUp(cls):
        """
        This method sets up the test class with ClientCommManager constructed.
        """
        cls.comm: ClientCommManager = ClientCommManager()
        print(cls.comm)

    def test_client_manager_singleton(self) -> None:
        """
        This test makes sure that the singleton is working so that error message will be given if the class is
        constructed more than once.
        """
        s = ClientCommManager()
        print(s)
        self.assertTrue(self.comm, s)

    def test_client_singleton_thread(self) -> None:
        """
        This test make sure that the singleton pattern is also avoiding ClientCommManager constructed more than twice
        in different threads. With the lock in __new__(cls) method, only one thread can access ClientCommManager class
        at a time.
        """
        x = threading.Thread(target=self.thread_function)
        x.start()
        x.join()  # have to joint thread x so that thread x2 can access ClientCommManager
        x2 = threading.Thread(target=self.thread_function)
        x2.start()

    def thread_function(self):
        """
        This method represent a thread for the test method 'test_client_singleton_thread'.
        """
        s = ClientCommManager()
        print(s)
        self.assertEqual(self.comm, s)

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
