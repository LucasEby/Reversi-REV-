from threading import Condition
from typing import Dict, Any, Optional

from common.client_server_protocols import update_elo_server_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager, DatabaseAccount


class UpdateELOClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that updates an account's elo in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_update_elo_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_dba: Optional[DatabaseAccount] = None

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """
        # Update account's elo in the database
        dba: DatabaseAccount = DatabaseAccount(
            account_id=None
            if "account_id" not in self._sent_message
            else self._sent_message["account_id"],
            elo=None
            if "new_elo" not in self._sent_message
            else self._sent_message["new_elo"],
        )
        DatabaseManager().update_account(
            callback=self.__elo_updated_callback,
            account_id=self._sent_message["account_id"],
            database_account=dba,
        )

        # Wait for database to complete tasks
        with self._db_complete_cv:
            while self._db_update_elo_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "protocol_type": update_elo_server_schema.schema["protocol_type"],
                "success": self._db_update_elo_success,
            }
        )
        return self._response_message

    def __elo_updated_callback(self, success: bool) -> None:
        """
        Callback for when the elo has finished being updated in the Database Manager
        :param success: Whether elo was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_update_elo_success = success
            self._db_complete_cv.notify()
