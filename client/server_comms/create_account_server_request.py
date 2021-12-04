from typing import Optional

from schema import Schema  # type: ignore

from client.model.account import Account
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import create_account_server_schema


class CreateAccountServerRequest(BaseServerRequest):
    def __init__(self, account: Account, password: str) -> None:
        """
        Create server request for creating account.
        :param account:    the account created for the user with preferences and elo initialized
        :param password:    the password that the user gives in
        """
        super().__init__()
        self._response_schema = create_account_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "username": account.get_username(),
                "password": password,
                "elo": account.elo,
                "pref_board_length": account.get_preference().get_board_size(),
                "pref_board_color": account.get_preference().get_board_color(),
                "pref_disk_color": account.get_preference().get_my_disk_color(),
                "pref_opp_disk_color": account.get_preference().get_opp_disk_color(),
                "pref_line_color": account.get_preference().get_line_color(),
                "pref_rules": str(account.get_preference().get_rule()),
                "pref_tile_move_confirmation": account.get_preference().get_tile_move_confirmation(),
            }
        )

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

    def get_account_id(self) -> Optional[int]:
        """
        Retrieves account ID from the server response if available
        :return: Account ID if available, None otherwise
        """
        if self.is_response_success() is True:
            return self._response_message["account_id"]
        else:
            return None
