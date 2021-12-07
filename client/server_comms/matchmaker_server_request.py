from typing import Optional

from schema import Schema  # type: ignore

from client.model.account import Account
from client.server_comms.base_server_request import BaseServerRequest
from common.client_server_protocols import matchmaker_server_schema


class MatchmakerServerRequest(BaseServerRequest):
    def __init__(self, account: Account) -> None:
        """
        Create server request for match making.

        :param account: the account whose account id is used for match making.
        """
        super().__init__()
        self._response_schema = matchmaker_server_schema
        self._send_message.update(
            {
                "protocol_type": self._response_schema.schema["protocol_type"],
                "my_account_id": account.id,
                "pref_rule": str(account.get_preference().get_rule()),
                "pref_board_size": account.get_preference().get_board_size(),
            }
        )

    def is_response_success(self) -> Optional[bool]:
        """
        Returns whether the response was a success.

        :return: True if success, false if failure, None if response is expected but hasn't arrived yet.
        """
        if self._response_success is None:
            return None
        elif self._response_success is False:
            return False
        else:
            return self._response_message["success"]

    def get_game_id(self) -> Optional[int]:
        """
        Retrieves game ID from the server response if available.

        :return: Game ID if available, None otherwise.
        """
        if self.is_response_success() is True:
            return self._response_message["game_id"]
        else:
            return None

    def get_opp_username(self) -> Optional[str]:
        """
        Retrieves opponent's username from the server response if available.

        :return: Opponent's username if available, None otherwise.
        """
        if self.is_response_success() is True:
            return self._response_message["opp_username"]
        else:
            return None

    def get_opp_elo(self) -> Optional[int]:
        """
        Retrieves opponent's elo from the server response if available.

        :return: Opponent's elo if available, None otherwise.
        """
        if self.is_response_success() is True:
            return self._response_message["opp_elo"]
        else:
            return None

    def get_player_term(self) -> Optional[int]:
        """
        Retrieves player's term from the server response if available.

        :return: Player's term if available, None otherwise.
        """
        if self.is_response_success() is True:
            return self._response_message["player_term"]
        else:
            return None
