import unittest
import socket
import json
from _thread import *


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_run_fake_server() -> None:
        """
        The test method imitates a server that listens for clients and puts them onto different threads.
        """
        # Run a server to listen for a connection and then close it
        server_sock = socket.socket()
        server_sock.bind(('127.0.0.1', 7777))
        server_sock.listen()
        print("Waiting for a connection, server started")
        while True:
            client, info = server_sock.accept()
            print("Connected to:", info)
            start_new_thread(threaded_client, (client, ))


def threaded_client(client):
    """
    Handles each client by printing out received messages from the client
    :param client: the client connection created
    """
    while True:
        try:
            data: str = client.recv(2048).decode()
            messages: [str] = data.split('$$')

            if not data:
                print("Disconnected")
                break
            else:
                # deal with all the protocols except the empty one at last
                for str_protocol in messages[:-1]:
                    protocol = json.loads(str_protocol)
                    for key, value in protocol.items():
                        print(key, value)
                    client.sendall((str_protocol + '$$').encode())
        except error as e:
            print(e)
            break
    print("Lost connection")
    client.close()


# def handle_json_msg(client) -> bool:
#     while True:
#         bb = client.recv(4096)
#         pcg = bb.decode()
#         pcg = pcg.split('$$')
#         # deal with all the protocols except the empty one at last
#         for str_protocol in pcg[:-1]:
#             client.sendall((str_protocol + '$$').encode())
#             protocol = json.loads(str_protocol)
#             for key, value in protocol.items():
#                 if value == "q":
#                     return True
#                 print(key, value)
#         return False


if __name__ == '__main__':
    unittest.main()
