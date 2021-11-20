from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseClientResponse(ABC):

    def __init__(self, message: Dict[str, Any]):
        """
        Base client response for all other client responses to build off
        Constructor ensures client response has a message
        :param message: Message sent to the server from the client
        """
        self._sent_message: Dict[str, Any] = message
        self._response_message: Dict[str, Any] = {}

    @abstractmethod
    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client once all server-related tasks have completed
        """
        pass


