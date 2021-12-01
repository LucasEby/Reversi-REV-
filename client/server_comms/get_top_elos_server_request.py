from typing import Optional, Tuple, List
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import get_top_elos_server_schema


class GetTopELOsServerRequest(BaseServerRequest):
    def __init__(self, num_elos: int = 10) -> None:
        """
        Creates server request for getting the top elos
        """
        super().__init__()
        self._response_schema = get_top_elos_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["num_elos"] = num_elos

    def is_response_success(self) -> Optional[bool]:
        """
        Returns whether the response was a success
        :return: True if success, false if failure, None if response is expected but hasn't arrived yet
        """
        if self._response_success is None:
            return None
        elif self._response_success is False:
            return False
        else:
            return self._response_message["success"]

    def get_top_elos(self) -> Optional[List[Tuple[str, int]]]:
        """
        Retrieves top ELOs from the server response if available
        :return: Top ELOs if available, None otherwise
        """
        if self.is_response_success() is True:
            top_elos: List[Tuple[str, int]] = self._response_message["top_elos"]
            return top_elos
        else:
            return None
