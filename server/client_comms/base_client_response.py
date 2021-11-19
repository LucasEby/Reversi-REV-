import socket
from abc import ABC, abstractmethod
from typing import Dict, Any, Callable


class BaseClientResponse(ABC):

    _respond_callback: Callable[[Any], None] = None

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
        self._handled = False

    @classmethod
    def register_respond_callback(cls, callback: Callable[[Any], None]) -> None:
        """
        Register a callback for sending a response back to the client
        :param callback: What function to call when response is ready to send back to client
        """
        cls._respond_callback = callback

    def is_handled(self) -> bool:
        """
        Return whether the client request has been handled
        """
        return self._handled

    @abstractmethod
    def handle_request(self) -> None:
        """
        Perform an initial handling of the request
        """
        self._handled = True

    @abstractmethod
    def respond(self) -> None:
        """
        Respond to the client once all server-related tasks have completed
        """
        pass


