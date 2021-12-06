from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema  # type: ignore

from common.client_server_protocols import (
    cancel_match_server_schema,
    cancel_match_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.matchmaker import Matchmaker


class CancelMatchClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that cancel the user's request for match making .

        :param message: Message info from client
        """
        super().__init__(message=message)
        self._complete_matchmaker: Condition = Condition()
        self._cancel_match_success: bool = False
        self._sent_message_schema: Schema = (
            cancel_match_client_schema  # from client side
        )
        self._response_message_schema: Schema = cancel_match_server_schema
        self._response_message["protocol_type"] = self._response_message_schema.schema[
            "protocol_type"
        ]

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager.
        """
        # Check schema of incoming message is ok; return false success to notify the client
        if not self._sent_message_schema.is_valid(self._sent_message):
            self._response_message["success"] = False
            return self._response_message

        # Provide information to Matchmaker for online player matching
        matchmaker: Matchmaker = Matchmaker()
        self._cancel_match_success = matchmaker.remove_user(
            self._sent_message["account_id"]
        )

        # Return the response message
        self._response_message.update(
            {
                "success": self._cancel_match_success,
            }
        )

        return self._response_message
