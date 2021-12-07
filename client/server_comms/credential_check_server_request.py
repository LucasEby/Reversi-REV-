from typing import Optional

from schema import Schema  # type: ignore

from client.model.account import Account
from client.model.preference import Preference
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import credential_check_server_schema


class CredentialCheckServerRequest(BaseServerRequest):
    def __init__(self, username: str) -> None:
        """
        Create server request for credential checking.

        :param username:    the username that the user gives in
        """
        super().__init__()
        self._response_schema: Schema = credential_check_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "username": username,
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

    def get_encrypted_password(self) -> Optional[str]:
        """
        Retrieves encrypted password from the server response if available

        :return: Encrypted password if available, None otherwise
        """
        if self.is_response_success() is True:
            return self._response_message["encrypted_password"]
        else:
            return None

    def get_account(self) -> Optional[Account]:
        """
        Get the account info from the server

        :return: Account info
        """
        if self.is_response_success() is True:
            account: Account = Account(
                username=self._send_message["username"],
                elo=self._response_message["elo"],
                account_id=self._response_message["account_id"],
            )
            preference: Preference = Preference()
            preference.set_board_size(self._response_message["pref_board_length"])
            preference.set_board_color(self._response_message["pref_board_color"])
            preference.set_my_disk_color(self._response_message["pref_disk_color"])
            preference.set_opp_disk_color(self._response_message["pref_opp_disk_color"])
            preference.set_line_color(self._response_message["pref_line_color"])
            preference.set_tile_move_confirmation(
                self._response_message["pref_tile_move_confirmation"]
            )
            account.set_preference(preference)
            return account
        else:
            return None
