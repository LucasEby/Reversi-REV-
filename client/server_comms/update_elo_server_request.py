from typing import Optional
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import update_elo_server_schema


class UpdateELOServerRequest(BaseServerRequest):
    def __init__(self, account_id: int, new_elo: int) -> None:
        """
        Creates server request for updating an account's elo
        """
        super().__init__()
        self._response_schema = update_elo_server_schema
        self._send_message["protocol_type"] = self._response_schema.schema[
            "protocol_type"
        ]
        self._send_message["account_id"] = account_id
        self._send_message["new_elo"] = new_elo

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

    def get_new_elo(self) -> Optional[int]:
        """
        Retrieves new elo from the server response if available (should be the same as elo sent to the server)
        :return: new elo if available, None otherwise
        """
        if self.is_response_success() is True:
            return self._response_message["new_elo"]
        else:
            return None
