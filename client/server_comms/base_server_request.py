from abc import ABC
from typing import Dict, Any, Optional

from schema import Schema

from client.server_comms.client_comms_manager import ClientCommsManager


class BaseServerRequest(ABC):
    def __init__(self) -> None:
        """
        Base server request for all other server requests to build off
        This constructor ensures all ServerRequests at least have send and response messages
        """
        self._send_message: Dict[str, Any] = {}
        self._response_message: Dict[str, Any] = {}
        self._response_success: Optional[bool] = None
        self._response_schema: Schema = Schema({})

    def send(self) -> None:
        """
        Sends the current message through the client comms manager, registering response callback in the process
        """
        if "protocol_type" in self._send_message:
            self._response_success = None
            ClientCommsManager().send(
                message=self._send_message,
                response_protocol_type=self._response_schema.schema["protocol_type"],
                callback=self._response_callback,
            )

    def _response_callback(self, success: bool, response: Dict[str, Any]) -> None:
        """
        Callback for the server response
        :param success: Whether server successfully responded. False would indicate a problem accessing the server
        :param response: Actual response from the server
        """
        self._response_success = success
        if self._response_success:
            if self._response_schema.is_valid(self._response_message):
                self._response_message = response
            else:
                self._response_success = success
