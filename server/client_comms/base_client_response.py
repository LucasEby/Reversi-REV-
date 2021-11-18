import socket
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseClientResponse(ABC):
    def __init__(self, message: Dict[Any], connection: socket, addr: str):
        """
        Base client response for all other client responses to build off
        Constructor ensures client response has a message
        :param message: Message sent to the server from the client
        :param connection: Socket connection with the client
        :param addr: Address of the client
        """
        self._sent_message: Dict[str, Any] = message
        self._response_message: Dict[str, Any] = {}
        self._client_connection: socket = connection
        self._client_address = addr

    @abstractmethod
    def execute(self) -> None:
        pass
