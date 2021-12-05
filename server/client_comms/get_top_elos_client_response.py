from threading import Condition
from typing import Dict, Any, Optional, Tuple, List

from common.client_server_protocols import get_top_elos_client_schema
from server.client_comms.base_client_response import BaseClientResponse
from server.database_management.database_manager import DatabaseManager


class GetTopELOsClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that gets some number of top ELOs in the database manager
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._db_get_top_elos_success: Optional[bool] = None
        self._db_complete_cv: Condition = Condition()
        self._retrieved_elos: Optional[List[Tuple[str, int]]] = None

    def respond(self) -> Dict[str, Any]:
        """
        Respond to the client through the server comms manager
        """
        DatabaseManager().get_top_elos(
            callback=self.__elos_retrieved_callback,
            get_username=True,
            get_elo=True,
            num_elos=self._sent_message["num_elos"],
        )

        # Wait for database to complete task
        with self._db_complete_cv:
            while self._db_get_top_elos_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "protocol_type": get_top_elos_client_schema.schema["protocol_type"],
                "success": self._db_get_top_elos_success,
                "top_elos": self._retrieved_elos,
            }
        )
        return self._response_message

    def __elos_retrieved_callback(
        self, success: bool, elos: List[Tuple[str, int]]
    ) -> None:
        """
        Callback for when the ELOs have finished being received from the Database Manager
        :param success: Whether retrieval was successful or not
        :param elos: List of top ELOs and corresponding usernames retrieved from database
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_top_elos_success = success
            if success is True:
                self._retrieved_elos = elos
            self._db_complete_cv.notify()
