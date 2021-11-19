import threading
import unittest
from _thread import *
from typing import Dict

from client.client_comm.client_comm_manager import ClientCommManager


class MyTestCase(unittest.TestCase):
    """
    This is a test class for client_comm_manager which tests the singleton pattern with threading and general functions
    such as sending, receiving and parsing messages.
    """

    comm = None

    def initialize_manager(self):
        """
        This method initializes a ClientCommManager.
        """
        self.comm: ClientCommManager = ClientCommManager()
        print(self.comm)

    def test_client_manager_singleton(self) -> None:
        """
        This test makes sure that the singleton is working so that error message will be given if the class is
        constructed more than once.
        """
        self.initialize_manager()
        s = ClientCommManager()
        print(s)
        self.assertEqual(self.comm, s)

    def test_client_singleton_thread_initialize_outside_threads(self) -> None:
        """
        This test make sure that the singleton pattern is also avoiding ClientCommManager constructed more than twice
        in different threads. With the lock in __new__(cls) method, only one thread can access ClientCommManager class
        at a time.
        """
        self.initialize_manager()
        x = threading.Thread(target=self.thread_function_initialize_outside_threads)
        x.start()
        x.join()  # have to joint thread x so that thread x2 can access ClientCommManager
        x2 = threading.Thread(target=self.thread_function_initialize_outside_threads)
        x2.start()

    def thread_function_initialize_outside_threads(self):
        """
        This method represent a thread for the test method 'test_client_singleton_thread_initialize_outside_threads'.
        """
        s = ClientCommManager()
        print(s)
        self.assertEqual(self.comm, s)

    # def test_client_singleton_thread(self) -> None:
    #     """
    #     This test make sure that the singleton pattern is also avoiding ClientCommManager constructed more than twice
    #     in different threads. And ClientCommManager is first initialized in thread x and retrieved in x2.
    #     """
    #     x = threading.Thread(target=self.thread_function)
    #     x.start()
    #     x.join()  # have to joint thread x so that thread x2 can access ClientCommManager
    #     x2 = threading.Thread(target=self.thread_function)
    #     x2.start()
    #
    # def thread_function(self):
    #     """
    #     This method represent a thread for the test method 'test_client_singleton_thread'.
    #     """
    #     s = ClientCommManager()
    #     print(s)

    # def test_run_client(self) -> None:
    #     """
    #     This test method can start a client side connection to check the login information with user input repeatedly.
    #     """
    #     self.initialize_manager()
    #     while True:
    #         self._username: str = input("Enter your username: ")
    #         self._password: str = input("Enter your password: ")
    #         if self._username == "q" or self._password == "q":
    #             self.comm.close_the_connection()
    #             break
    #         self.send_login(self._username, self._password)
    #         # start_new_thread(self.comm.run, ())
    #         communication = ClientCommManager()
    #         start_new_thread(communication.run, ())

    def test_run_client(self) -> None:
        """
        This test method starts a client side connection to check the login information.
        """
        self.initialize_manager()
        self._username: str = "username"
        self._password: str = "password"
        self.send_login(self._username, self._password)
        # start_new_thread(self.comm.run, ())
        communication = ClientCommManager()
        start_new_thread(communication.run, ())

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
        self.comm.send(data, "server_login", self.print_method_to_test)

    def print_method_to_test(self, success: bool, protocol: Dict[str, str]) -> None:
        """
        This method represents a callable passed in with login message in the last line of send_login.
        """
        # the print out lines can be used with the repeating test method to check interactively
        # print("This is a method only for testing if CALLABLE functions well.")
        # print("Message transfer status: " + str(success))
        # print("username: " + protocol["username"])
        # print("password: " + protocol["password"])
        self.assertEqual(self._username, protocol["username"])
        self.assertEqual(self._password, protocol["password"])


if __name__ == "__main__":
    unittest.main()
