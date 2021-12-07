from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema  # type: ignore

from common.client_server_protocols import (
    matchmaker_server_schema,
    matchmaker_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.matchmaker import Matchmaker
from server.database_management.database_manager import DatabaseManager, DatabaseAccount


class MatchmakerClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that match users who want to play game with other online users.

        :param message: Message info from client
        """
        super().__init__(message=message)
        self._complete_matchmaker: Condition = Condition()
        self._game_id: Optional[int] = None
        self._opp_account_id: Optional[int] = None
        self._player_term: Optional[
            int
        ] = None  # whether the player will be the first or second to play
        self._db_complete_cv: Condition = Condition()
        self._db_get_opp_account_success: Optional[bool] = None
        self._sent_message_schema: Schema = matchmaker_client_schema  # from client side
        self._response_message_schema: Schema = matchmaker_server_schema
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
        matchmaker.match_user(
            self._sent_message["my_account_id"],
            self._sent_message["pref_rule"],
            self._sent_message["pref_board_size"],
            self.__wait_for_match_callback,
        )

        # Wait for matchmaker to complete task
        with self._complete_matchmaker:
            while self._opp_account_id is None:
                self._complete_matchmaker.wait()

        # print("game_id: " + str(self._game_id))
        # print("opp_account_id: " + str(self._opp_account_id))

        # Check if an opponent id is returned to retrieve information; return false message directly if it is none
        if self._opp_account_id is None or self._game_id is None:
            self._response_message["success"] = False
            return self._response_message

        DatabaseManager().get_account(
            key=self._opp_account_id,
            callback=self.__opp_account_retrieved_callback,
            get_username=True,
            get_elo=True,
        )

        with self._db_complete_cv:
            while self._db_get_opp_account_success is None:
                self._db_complete_cv.wait()

        # Return the response message
        self._response_message.update(
            {
                "success": False
                if not self._db_get_opp_account_success or self._game_id is None
                else True,
                "game_id": 0 if self._game_id is None else self._game_id,
                "opp_username": None
                if self._retrieved_dba.username is None
                else self._retrieved_dba.username,
                "opp_elo": 0
                if self._retrieved_dba.elo is None
                else self._retrieved_dba.elo,
                "player_term": 0 if self._player_term is None else self._player_term,
            }
        )

        return self._response_message

    def __wait_for_match_callback(
        self, game_id: Optional[int], opp_account_id: int, player_term: int
    ) -> None:
        """
        Callback for when current player find a match in the player list in Matchmaker class. It will set the created
        game id, opponent's account id, and current player's term in the online game.

        :param game_id: the game id for the online game.
        :param opp_account_id: the account id for opponent.
        :param player_term: the player's term in this online game.
        """
        # Notify class that database has completed its task
        with self._complete_matchmaker:
            self._game_id = game_id
            self._opp_account_id = opp_account_id
            self._player_term = player_term
            self._complete_matchmaker.notify()

    def __opp_account_retrieved_callback(
        self, success: bool, dba: DatabaseAccount
    ) -> None:
        """
        Callback for account information in the database manager has been retrieved
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_get_opp_account_success = success
            if success is True:
                self._retrieved_dba = dba
            self._db_complete_cv.notify()
