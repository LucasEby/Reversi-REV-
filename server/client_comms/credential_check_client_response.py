from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema  # type: ignore

from common.client_server_protocols import (
    credential_check_server_schema,
    credential_check_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseAccount


class CredentialCheckClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that creates a new game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_credential_check_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dba: Optional[DatabaseAccount] = None
        self._sent_message_schema: Schema = (
            credential_check_client_schema  # from client side
        )
        self._response_message_schema: Schema = credential_check_server_schema
        self._response_message["protocol_type"] = self._response_message_schema.schema[
            "protocol_type"
        ]

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """
        # Check schema of incoming message is ok; return false success to notify the client
        if not self._sent_message_schema.is_valid(self._sent_message):
            self._response_message["success"] = False
            return self._response_message

        # Get the username and password
        DatabaseManager().get_account(
            callback=self.__credential_retrieved_callback,
            key=self._sent_message["username"],
            get_account_id=True,
            get_password=True,
            get_elo=True,
            get_pref_board_length=True,
            get_pref_board_color=True,
            get_pref_disk_color=True,
            get_pref_opp_disk_color=True,
            get_pref_line_color=True,
            get_pref_rules=True,
            get_pref_tile_move_confirmation=True,
        )

        # Wait for database manager to complete task
        with self._db_complete_cv:
            while self._db_credential_check_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        if self._retrieved_dba is not None:
            self._response_message.update(
                {
                    "success": self._db_credential_check_success,
                    "encrypted_password": self._retrieved_dba.password,
                    "account_id": self._retrieved_dba.account_id,
                    "elo": self._retrieved_dba.elo,
                    "pref_board_length": self._retrieved_dba.pref_board_length,
                    "pref_board_color": self._retrieved_dba.pref_board_color,
                    "pref_disk_color": self._retrieved_dba.pref_disk_color,
                    "pref_opp_disk_color": self._retrieved_dba.pref_opp_disk_color,
                    "pref_line_color": self._retrieved_dba.pref_line_color,
                    "pref_rules": self._retrieved_dba.pref_rules,
                    "pref_tile_move_confirmation": self._retrieved_dba.pref_tile_move_confirmation,
                }
            )
        else:
            self._response_message.update(
                {
                    "success": False,
                    "encrypted_password": "",
                    "account_id": 0,
                    "elo": 0,
                    "pref_board_length": 0,
                    "pref_board_color": "",
                    "pref_disk_color": "",
                    "pref_opp_disk_color": "",
                    "pref_line_color": "",
                    "pref_rules": "",
                    "pref_tile_move_confirmation": False,
                }
            )

        return self._response_message

    def __credential_retrieved_callback(
        self, success: bool, dba: DatabaseAccount
    ) -> None:
        """
        Callback for account information in the database manager has been retrieved
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_credential_check_success = success
            if success is True:
                self._retrieved_dba = dba
            self._db_complete_cv.notify()
