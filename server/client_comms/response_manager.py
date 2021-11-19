import socket
from queue import Queue
from threading import Lock
from typing import Dict, Any

from common.client_server_protocols import create_game_client_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.client_comms.create_game_client_response import CreateGameClientResponse
from server.client_comms.server_comms_manager import ServerCommsManager


class ResponseManager:

    _instance = None
    _lock: Lock = Lock()
    _queue: Queue = Queue()
    _protocol_type_response_dict: Dict[str, BaseClientResponse] = {
        create_game_client_schema.schema["protocol_type"]: CreateGameClientResponse
    }

    def __new__(cls, *args, **kwargs):
        """
        Ensure RequestManager is a singleton
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ResponseManager, cls).__new__(cls)
                    # Register callback in server comms manager to handle client request
                    ServerCommsManager().register_handle_response_callback(
                        cls._instance._handle_response
                    )
                    # Register callback in base client response to queue a response back to the client
                    BaseClientResponse.register_respond_callback(cls._instance._queue.put)
        return cls._instance

    def run(self) -> None:
        """
        Keep running client responses from the queue
        """
        response: BaseClientResponse = self._queue.get()
        if not response.is_handled():
            response.handle_request()
        else:
            response.respond()

    def _handle_response(
        self, message: Dict[str, Any], connection: socket, addr: str
    ) -> None:
        """
        Adds a response to the queue for future execution based on the protocol type of the given message
        :param message: Message passed from the server comms manager
        """
        # Check prototype type in message is valid
        if "protocol_type" not in message:
            return
        if message["protocol_type"] not in self._protocol_type_response_dict:
            return
        # Queue response based on protocol type of incoming message
        new_response: BaseClientResponse = globals()[
            type(self._protocol_type_response_dict[message["protocol_type"]]).__name__
        ](message, connection, addr)
        self._queue.put(new_response)
