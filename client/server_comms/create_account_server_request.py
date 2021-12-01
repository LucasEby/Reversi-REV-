from typing import Optional

from client.model.preference import Preference
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import credential_check_server_schema


class CreateAccountServerRequest(BaseServerRequest):
    def __init__(self, username: str, password: str, preference: Preference) -> None:
        """
        Create server request for creating account.
        :param username:    the username that the user gives in
        :param password:    the password that the user gives in
        :param preference:  initial preference for new user
        """
        super().__init__()
        self._response_schema = credential_check_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "username": username,
                "password": password,
                "elo": 0,
                "pref_board_length": preference.get_board_size(),
                "pref_board_color": preference.get_board_color(),
                "pref_disk_color": preference.get_my_disk_color(),
                "pref_opp_disk_color": preference.get_opp_disk_color(),
                "pref_line_color": preference.get_line_color(),
                "pref_rules": str(preference.get_rule()),
                "pref_tile_move_confirmation": preference.get_tile_move_confirmation(),
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
