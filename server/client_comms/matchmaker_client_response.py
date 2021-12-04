from threading import Condition
from typing import Dict, Any, Optional

from schema import Schema  # type: ignore

from common.client_server_protocols import (
    matchmaker_server_schema,
    matchmaker_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.matchmaker import Matchmaker


class MatchmakerClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that match users who want to play game with other online users
        :param message: Message info from client
        """
        super().__init__(message=message)
        self._complete_matchmaker: Condition = Condition()
        self._opp_account_id: Optional[int] = None
        self._game_id: Optional[int] = None
        # self._db_complete_cv: Condition = Condition()
        # self._db_matchmaker_create_game_success: Optional[bool] = None
        # self._db_matchmaker_retrieve_game_success: Optional[bool] = None
        # self._retrieved_dbg: Optional[DatabaseGame] = None
        self._sent_message_schema: Schema = matchmaker_client_schema  # from client side
        self._response_message_schema: Schema = matchmaker_server_schema
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

        # Provide information to Matchmaker for online player matching
        matchmaker: Matchmaker = Matchmaker()
        matchmaker.match_user(
            self._sent_message["account_id"],
            self._sent_message["pref_rule"],
            self._sent_message["pref_board_size"],
            self.__wait_for_match_callback,
        )

        # Wait for matchmaker to complete task
        with self._complete_matchmaker:
            while self._opp_account_id and self._game_id is None:
                self._complete_matchmaker.wait()

        # Return the response message
        self._response_message.update(
            {
                "success": False
                if self._opp_account_id or self._game_id is None
                else True,
                "game_id": 0 if self._game_id is None else self._game_id,
                "opp_account_id": 0
                if self._opp_account_id is None
                else self._opp_account_id,
            }
        )
        return self._response_message

        # # Add rule and account ids to DatabaseGame for creating game
        # # TODO: do we need to specify board size in database as it is asked when matching players
        # # TODO: probably need to pass in another parameter to specify p1 and p2
        # dbg: DatabaseGame = DatabaseGame(
        #     rules=self._sent_message["pref_rule"],
        #     p1_account_id=self._sent_message["account_id"],
        #     p2_account_id=self._opp_account_id,
        # )
        # DatabaseManager().create_game(
        #     callback=self.__matchmaker_game_created_callback,
        #     database_game=dbg,
        # )
        # DatabaseManager().get_game(
        #     key=self._sent_message[
        #         "p1_account_id"
        #     ],  # TODO: need to coordinate with the assigned player number
        #     callback=self.__matchmaker_game_retrieved_callback,
        # )
        #
        # # Wait for database manager to complete task
        # with self._db_complete_cv:
        #     while (
        #         self._db_matchmaker_create_game_success is None
        #         or self._db_matchmaker_retrieve_game_success is None
        #     ):
        #         self._db_complete_cv.wait()
        #
        # # Return the response message
        # self._response_message.update(
        #     {
        #         "success": self._db_matchmaker_create_game_success
        #         and self._db_matchmaker_retrieve_game_success,
        #         "game_id": 0
        #         if self._retrieved_dbg is None
        #         else self._retrieved_dbg.game_id,
        #         "opp_account_id": 0
        #         if self._opp_account_id is None
        #         else self._opp_account_id,
        #     }
        # )
        # return self._response_message

    def __wait_for_match_callback(self, opp_account_id: int, game_id: int) -> None:
        """
        Callback for when current player find a match in the player list in Matchmaker class
        :param opp_account_id:  the account id for opponent
        """
        # Notify class that database has completed its task
        with self._complete_matchmaker:
            self._opp_account_id = opp_account_id
            self._game_id = game_id
            self._complete_matchmaker.notify()

    # def __matchmaker_game_created_callback(self, success: bool) -> None:
    #     """
    #     Callback for when the fame has finished being created in the Database Manager
    #     :param success: Whether game was created successfully
    #     """
    #     # Notify class that database has completed its task
    #     with self._db_complete_cv:
    #         self._db_matchmaker_create_game_success = success
    #         self._db_complete_cv.notify()
    #
    # def __matchmaker_game_retrieved_callback(
    #     self, success: bool, dbg: DatabaseGame
    # ) -> None:
    #     """
    #     Callback for when the game has finished being received from the Database Manager
    #     :param success: Whether retrieval was successful or not
    #     :param dbg: Database game retrieved from database
    #     """
    #     # Notify class that database has completed its task
    #     with self._db_complete_cv:
    #         self._db_matchmaker_retrieve_game_success = success
    #         if success is True:
    #             self._retrieved_dbg = dbg
    #         self._db_complete_cv.notify()
