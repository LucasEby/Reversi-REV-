from typing import Optional

from schema import Schema  # type: ignore

from client.model.account import Account
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import cancel_match_server_schema


class CancelMatchServerRequest(BaseServerRequest):
    def __init__(self, account: Account) -> None:
        """
        Create server request for canceling match making.

        :param account: the account whose account id is used for canceling match making
        """
        super().__init__()
        self._response_schema = cancel_match_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "my_account_id": account.id,
            }
        )

    def is_response_success(self) -> Optional[bool]:
        """
        Returns whether the response was a success.

        :return: True if success, false if failure, None if response is expected but hasn't arrived yet
        """
        if self._response_success is None:
            return None
        elif self._response_success is False:
            return False
        else:
            return self._response_message["success"]
