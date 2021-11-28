from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema

from common.client_server_protocols import (
    save_preferences_server_schema,
    save_preferences_client_schema,
)
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseAccount, DatabaseManager


class SavePreferencesClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that saves preferences to an existing account
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._sent_message_schema: Schema = save_preferences_client_schema
        self._response_message_schema: Schema = save_preferences_server_schema
        self._response_message["protocol_type"] = self._response_message_schema.schema[
            "protocol_type"
        ]

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        :return Message to send to client
        """
        # Check schema of incoming message is ok
        if not self._sent_message_schema.is_valid(self._sent_message):
            self._response_message["success"] = False
            return self._response_message

        # Update preferences in database
        dba: DatabaseAccount = DatabaseAccount(
            pref_board_length=self._sent_message["pref_board_length"],
            pref_board_color=self._sent_message["pref_board_color"],
            pref_disk_color=self._sent_message["pref_disk_color"],
            pref_opp_disk_color=self._sent_message["pref_opp_disk_color"],
            pref_line_color=self._sent_message["pref_line_color"],
            pref_rules=self._sent_message["pref_rules"],
            pref_tile_move_confirmation=self._sent_message[
                "pref_tile_move_confirmation"
            ],
        )
        DatabaseManager().update_account(
            callback=self.__account_updated_callback,
            account_id=self._sent_message["account_id"],
            database_account=dba,
        )

        # Wait for database manager to complete task
        with self._db_complete_cv:
            while self._db_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message["success"] = self._db_success
        return self._response_message

    def __account_updated_callback(self, success: bool) -> None:
        """
        Callback for when the account has finished being saved in the database manager
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_success = success
            self._db_complete_cv.notify()
