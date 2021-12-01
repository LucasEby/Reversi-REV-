from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema

from common.client_server_protocols import (
    create_account_server_schema,
    create_account_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseAccount


class CreateAccountClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that creates a new game in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_create_account_success: Optional[bool] = None
        self._db_get_account_id_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dba: Optional[DatabaseAccount] = None
        self._sent_message_schema: Schema = (
            create_account_client_schema  # from client side
        )
        self._response_message_schema: Schema = create_account_server_schema
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

        dba: DatabaseAccount = DatabaseAccount(
            username=self._sent_message["username"],
            password=self._sent_message["password"],
            elo=self._sent_message["elo"],
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
        DatabaseManager().create_account(
            callback=self.__account_created_callback,
            database_account=dba,
        )
        DatabaseManager().get_account(
            key=self._sent_message["username"],
            callback=self.__account_retrieved_callback,
            get_account_id=True,
        )

        # Wait for database manager to complete task
        with self._db_complete_cv:
            while (
                self._db_create_account_success is None
                or self._db_get_account_id_success is None
            ):
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "success": self._db_create_account_success,
                "create_account": False,
                "account_id": 0
                if self._retrieved_dba is None
                else self._retrieved_dba.account_id,
            }
        )
        return self._response_message

    def __account_created_callback(self, success: bool) -> None:
        """
        Callback for when the game has finished being created in the Database Manager
        :param success: Whether game was created successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_create_account_success = success
            self._db_complete_cv.notify()

    def __account_retrieved_callback(self, success: bool, dba: DatabaseAccount) -> None:
        """
        Callback for account information in the database manager has been retrieved
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_account_id_success = success
            if success is True:
                self._retrieved_dba = dba
            self._db_complete_cv.notify()
