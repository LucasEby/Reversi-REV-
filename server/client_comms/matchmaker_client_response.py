from datetime import datetime
from threading import Condition
from typing import Dict, Any, Optional, Callable, List

from schema import Schema  # type: ignore

from common.client_server_protocols import (
    matchmaker_server_schema,
    matchmaker_client_schema,
)

from server.client_comms.base_client_response import BaseClientResponse
from server.matchmaker import Matchmaker
from server.database_management.database_manager import (
    DatabaseManager,
    DatabaseAccount,
    DatabaseGame,
)


class MatchmakerClientResponse(BaseClientResponse):
    def __init__(self, message: Dict[str, Any]) -> None:
        """
        C'tor for response handler that match users who want to play game with other online users.

        :param message: Message info from client
        """
        super().__init__(message=message)
        self._complete_matchmaker: Condition = Condition()
        self._game_id: int = 0
        self._opp_account_id: Optional[int] = None
        self._player_term: Optional[
            int
        ] = None  # whether the player will be the first or second to play
        self._matchmaker_callback: Optional[Callable[..., None]] = None
        self._db_complete_cv: Condition = Condition()
        self._db_matchmaker_create_game_success: Optional[bool] = None
        self._db_matchmaker_retrieve_game_success: Optional[bool] = None
        self._db_game_id: Optional[int] = 0
        self._db_complete_get_opp_account: Condition = Condition()
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

        # Check if an opponent id is returned to retrieve information; return false message directly if it is none
        if (
            self._opp_account_id is None
            or (self._game_id == 0 and self._matchmaker_callback is None)
            or (self._game_id != 0 and self._matchmaker_callback is not None)
        ):
            self._response_message["success"] = False
            return self._response_message

        if self._game_id == 0 and self._matchmaker_callback is not None:
            dbg: DatabaseGame = DatabaseGame(
                complete=False,
                board_state=self.__matchmaker_initialize_board(),
                rules=self._sent_message["pref_rule"],
                next_turn=1,
                p1_account_id=self._sent_message["my_account_id"],
                p2_account_id=self._opp_account_id,
                last_save=datetime.now(),
            )
            DatabaseManager().create_game(
                callback=self.__matchmaker_game_created_callback,
                database_game=dbg,
            )
            DatabaseManager().get_game(
                key=self._sent_message["my_account_id"],
                callback=self.__matchmaker_game_retrieved_callback,
                last_game=True,
                get_game_id=True,
            )

            # Wait for database manager to complete task
            with self._db_complete_cv:
                while (
                    self._db_matchmaker_create_game_success is None
                    or self._db_matchmaker_retrieve_game_success is None
                ):
                    self._db_complete_cv.wait()

            self._matchmaker_callback(
                self._db_game_id, self._sent_message["my_account_id"], 2, None
            )
        elif self._game_id is not None and self._matchmaker_callback is None:
            self._db_game_id = self._game_id

        DatabaseManager().get_account(
            key=self._opp_account_id,
            callback=self.__opp_account_retrieved_callback,
            get_username=True,
            get_elo=True,
        )

        with self._db_complete_get_opp_account:
            while self._db_get_opp_account_success is None:
                self._db_complete_get_opp_account.wait()

        # Return the response message
        self._response_message.update(
            {
                "success": False
                if not self._db_get_opp_account_success or self._db_game_id is None
                else True,
                "game_id": 0 if self._db_game_id == 0 else self._db_game_id,
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
        self,
        game_id: int,
        opp_account_id: int,
        player_term: int,
        callback: Optional[Callable[..., Any]],
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
            self._matchmaker_callback = callback
            self._complete_matchmaker.notify()

    def __opp_account_retrieved_callback(
        self, success: bool, dba: DatabaseAccount
    ) -> None:
        """
        Callback for account information in the database manager has been retrieved
        :param success: Whether game was updated successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_get_opp_account:
            self._db_get_opp_account_success = success
            if success is True:
                self._retrieved_dba = dba
            self._db_complete_get_opp_account.notify()

    def __matchmaker_game_created_callback(self, success: bool) -> None:
        """
        Callback for when the fame has finished being created in the Database Manager

        :param success: Whether game was created successfully
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_matchmaker_create_game_success = success
            self._db_complete_cv.notify()

    def __matchmaker_game_retrieved_callback(
        self, success: bool, dbg: DatabaseGame
    ) -> None:
        """
        Callback for when the game has finished being received from the Database Manager

        :param success: Whether retrieval was successful or not
        :param dbg: Database game retrieved from database
        """
        # Notify class that database has completed its task
        with self._db_complete_cv:
            self._db_matchmaker_retrieve_game_success = success
            if success is True:
                self._db_game_id = dbg.game_id
                self._db_game_id = dbg.game_id
            self._db_complete_cv.notify()

    def __matchmaker_initialize_board(self) -> List[List[int]]:
        size: int = self._sent_message["pref_board_size"]
        cells: List[List[int]] = [[0] * size for _ in range(size)]
        # initialize the four starting disks at the center of the board
        cells[size // 2][size // 2 - 1] = 1
        cells[size // 2 - 1][size // 2] = 1
        cells[size // 2 - 1][size // 2 - 1] = 2
        cells[size // 2][size // 2] = 2
        return cells
