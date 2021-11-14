from typing import List
import json
import traceback
import socket


ADDRESS = ('127.0.0.1', 7777)   # the address to connect to the server (the one right now is just for testing)


class ClientCommManager:
    """
    This ClientCommManager class initializes connection to the server and provides methods that send message to the
    server or handle the received message.
    """
    def __init__(self, receive_key: str, callback: str) -> None:
        """
        Construct a class serves as the client side of the network connection.
        """
        self.receive_key: str = receive_key  # TODO: what is receive key for (have it in the class diagram)
        self.callback: str = callback        # TODO: what is callback for (have it in the class diagram)
        self.client: socket = socket.socket()
        self.client.connect(ADDRESS)
        self.__returned_message: dict = {}   # message returned by the server

    def send(self, message: dict) -> None:
        """
        Send out the message to the server for communication and the message will be encapsulated before transmission.
        After message is sent out, it will wait for response and handle it.
        Protocol types include:
            - client_login
            - client_guest
            - client_create_account
            - client_update_board
            - client_get_elo
            - client_match_request
        :param message: the message to be sent to the server in dictionary; it should at least have 'protocol_type'
                        specified
        :raise ValueError: if the passed in message does not contain a 'protocol_type'
        """
        # check if the message have specified protocol type and throw ValueError if
        if not message['protocol_type']:
            raise ValueError("Message must have a protocol_type.")
        # put '$$' to signify end of message and encapsulate the message
        json_msg: str = json.dumps(message, ensure_ascii=False) + '$$'
        #
        try:
            self.client.send(json_msg.encode())
            self._handle_receive()
        except socket.error as e:
            print(e)

    def _handle_receive(self) -> None:
        """
        This method gets back the message from the server and handles it.
        """
        pcg: bytes = self.client.recv(2048)
        # if the received package is empty, connection lost should be handled
        if len(pcg) == 0:
            self.client.close()
            # TODO: deal with connection lost
            traceback.print_exc()
            pass
        # parse and deal with the data
        self.__parse_data(pcg)

    def __parse_data(self, pcg: bytes) -> None:
        """
        This method decodes and splits the package into protocols. Protocols in the package will be parsed and executed
        one after another.
        :param pcg: the received package directly from the server in bytes
        """
        protocols: str = pcg.decode()
        protocols: List[str] = protocols.split('$$')
        if protocols.__len__() > 2:
            raise Exception("Multiple messages are received at once.")
        protocol: dict = json.loads(protocols[0])
        self.__deal_with_data(protocol)
        self.__returned_message = protocol

    def get_returned_message(self, key: str) -> str:
        """
        Get specific value in the returned message with provided key.
        :param key: the key to access the value in the returned dictionary
        :returns:   the value corresponding to the given key
        """
        return self.__returned_message[key]

    def close_the_connection(self) -> None:
        """
        Closing the socket.
        """
        self.client.close()
        print("Connection on the client side is closed.")

    @staticmethod
    def __deal_with_data(protocol: dict) -> None:
        """
        Trying to parse the received data and make operations accordingly, but was only printing for check right now.
        :param protocol: parsed protocol at least includes 'protocol_type' and it might contain more keys and values
        """
        if protocol['protocol_type'] == 'client_login':  # TODO: change 'protocol_type' accordingly
            # 'server_login' gives back result
            print("Client received login feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_match_request':  # TODO: change 'protocol_type' accordingly
            # 'server_match_request' gives back the matching opponent
            print("Client received match_request feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_move':  # TODO: change 'protocol_type' accordingly
            # 'server_move' gives opponent's move
            print("Client received move feedback:")
            for key, value in protocol.items():
                print(key, value)
        elif protocol['protocol_type'] == 'client_elo':  # TODO: change 'protocol_type' accordingly
            # 'server_elo' gives opponent's move
            print("Client received elo feedback:")
            for key, value in protocol.items():
                print(key, value)
