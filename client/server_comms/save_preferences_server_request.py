from typing import Optional

from schema import Schema  # type: ignore

from client.model.account import Account
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import save_preferences_server_schema


class SavePreferencesServerRequest(BaseServerRequest):
    def __init__(self, account: Account) -> None:
        """
        Creates server request for saving preferences
        :param account: Account whose preferences should be saved
        """
        super().__init__()
        self._response_schema: Schema = save_preferences_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "account_id": account.id,
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
