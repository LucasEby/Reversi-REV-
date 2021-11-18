from threading import Lock
from typing import List, Dict, Callable, Any
import json
import traceback
import socket
from client.config.config_reader import ConfigReader


class ClientCommManager:
    """
    This ClientCommManager class initializes connection to the server and provides methods that send message to the
    server or handle the received message.
    """

    # initialize singleton as None if ClientCommManager class has not been constructed ever
    _singleton: "ClientCommManager" = None
    _lock: Lock = Lock()

    def __new__(cls) -> "ClientCommManager":
        """
        Create a ClientCommManager object. Initialized object will be return if it already exists, otherwise a new one
        will be initialized.
        """
        with cls._lock:
            if not cls._singleton:
                cls._singleton = super(ClientCommManager, cls).__new__(cls)
            return cls._singleton

    def __init__(self) -> None:
        """
        Initialize the class which serves as the client side of the network connection.
        """
        self.client: socket = socket.socket()
        address = ConfigReader().get_server_info()
        self.client.connect(address)
        self._callback_map: Dict[str, List[Callable[[], Any]]] = {}

    def send(
        self,
        message: Dict[str, Any],
        response_protocol_type: str,
        callback: Callable[[], Any],
    ) -> None:
        """
        Send out the message to the server for communication and the message will be encapsulated before transmission.
        After message is sent out, it will wait for response and handle it.

        :param message: the message to be sent to the server in dictionary; it should at least have 'protocol_type'
                        specified
        :param response_protocol_type: expected protocol type from the server to identify which callback to use
        :param callback: the function to call when you receive a message of a certain 'protocol_type'
        :raise ValueError: if the passed in message does not contain a 'protocol_type'
        """
        # check if the message have specified protocol type and throw ValueError if
        if not response_protocol_type or not message["protocol_type"]:
            raise ValueError("Message must have a protocol_type.")
        if response_protocol_type not in self._callback_map:
            self._callback_map[response_protocol_type] = []
        self._callback_map[response_protocol_type].append(
            callback
        )  # append the callback to the _callback_map
        # put '$$' to signify end of message and encapsulate the message
        json_msg: str = json.dumps(message, ensure_ascii=False) + "$$"
        # send the json message to server
        try:
            self.client.send(json_msg.encode())
        except socket.error as e:
            print(e)

    def run(self):
        """
        Call the __handle_receive method in a forever loop so that it will keep listening for the message from server.
        """
        while True:
            self.__handle_receive()

    def __handle_receive(self) -> None:
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
        protocols: List[str] = protocols.split("$$")
        # parse all the protocols if multiple are received
        for str_protocol in protocols[:-1]:
            protocol: Dict[str, str] = json.loads(str_protocol)
            self.__deal_with_data(protocol)

    def __deal_with_data(self, protocol: Dict[str, str]) -> None:
        """
        Callback the functions with parsed returned protocol.

        :param protocol: parsed protocol at least includes 'protocol_type' and it might contain more keys and values
        """
        if protocol.__len__() == 1:
            self._callback_map[protocol["protocol_type"]][0](False, protocol)
        else:
            # get the first callable in the list corresponding to 'protocol_type' and run it with corresponding
            # parameters
            self._callback_map[protocol["protocol_type"]][0](True, protocol)
        self._callback_map[protocol["protocol_type"]].pop(
            0
        )  # get rid of the first callable in the list

    def close_the_connection(self) -> None:
        """
        Closing the socket.
        """
        self.client.close()
        print("Connection on the client side is closed.")
