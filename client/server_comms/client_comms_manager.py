from queue import Queue
from threading import Lock
from typing import List, Dict, Callable, Any, Optional
import json
import socket
from client.config.config_reader import ConfigReader, ServerInfo


class ClientCommsManager:
    """
    This ClientCommManager class initializes connection to the server and provides methods that send message to the
    server or handle the received message.
    """

    # initialize singleton as None if ClientCommManager class has not been constructed ever
    _singleton = None
    _lock: Lock = Lock()
    _client: socket.socket = socket.socket()
    _callback_map: Dict[str, List[Callable[[bool, Any], None]]] = {}
    _send_queue: Queue = Queue()
    _connected_to_server: bool = False

    def __new__(cls):
        """
        Create a ClientCommManager object. Initialized object will be return if it already exists, otherwise a new one
        will be initialized.
        """
        if not cls._singleton:
            with cls._lock:
                if not cls._singleton:
                    cls._singleton = super(ClientCommsManager, cls).__new__(cls)
        return cls._singleton

    def __connect_to_server(self) -> None:
        """
        Tries to connect to server. Putting in own function allows chance to re-connect if failed
        """
        address: Optional[ServerInfo] = ConfigReader().get_server_info()
        if address is None:
            return
        try:
            # Create a new socket (if old failed, we need a new one)
            self._client = socket.socket()
            self._client.connect((address.server_ip, address.server_port))
            self._connected_to_server = True
        except Exception:
            self._connected_to_server = False

    def send(
        self,
        message: Dict[str, Any],
        response_protocol_type: str,
        callback: Callable[..., None],
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
        # check if the message have specified protocol type and throw ValueError if not
        if "protocol_type" not in message:
            raise ValueError("Message must have a protocol_type.")
        # Add sending info to the queue
        self._send_queue.put((message, response_protocol_type, callback))

    def run(self):
        """
        Call the __send __handle_receive method in a forever loop
        so that it will keep sending then listening for the message to/from server.
        """
        self._client.settimeout(None)
        while True:
            if self._connected_to_server:
                self.__send()
                self.__handle_receive()
            else:
                self.__connect_to_server()

    def __send(self) -> None:
        """
        Takes any messages dropped off to send and sends them.
        This is in own function so all socket operations occur in one thread.
        """
        # Get info from queue
        message, response_protocol_type, callback = self._send_queue.get()
        # Add a new key to the _callback_map if passed-in response_protocol_type is not a key in the map yet
        if response_protocol_type not in self._callback_map:
            self._callback_map[response_protocol_type] = []
        self._callback_map[response_protocol_type].append(
            callback
        )  # append the callback to the _callback_map
        # Put '$$' to signify end of message and encapsulate the message
        json_msg: str = json.dumps(message, ensure_ascii=False) + "$$"
        # Send the json message to server (let comms manager do its thing with the dropped-off message)
        try:
            self._client.send(json_msg.encode())
        except socket.error as e:
            self._callback_map[response_protocol_type][0](False, response_protocol_type)
            self._callback_map[response_protocol_type].pop(0)
            self._client.close()
            self._connected_to_server = False
            print(e)

    def __handle_receive(self) -> None:
        """
        This method gets back the message from the server and handles it.
        """
        try:
            pcg: bytes = self._client.recv(2048)
            # Parse and deal with the data
            self.__parse_data(pcg)
        except socket.error as e:
            self._client.close()
            self._connected_to_server = False
            print(e)

    def __parse_data(self, pcg: bytes) -> None:
        """
        This method decodes and splits the package into protocols. Protocols in the package will be parsed and executed
        one after another.

        :param pcg: the received package directly from the server in bytes
        """
        protocols: List[str] = pcg.decode().split("$$")
        # parse all the protocols if multiple are received
        for str_protocol in protocols[:-1]:
            protocol: Dict[str, Any] = json.loads(str_protocol)
            self.__deal_with_data(protocol)

    def __deal_with_data(self, protocol: Dict[str, Any]) -> None:
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
        self._client.close()
        print("Connection on the client side is closed.")
