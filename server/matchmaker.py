from dataclasses import dataclass
from datetime import datetime
from threading import Lock, Condition
from typing import List, Tuple, Callable, Optional

from server.database_management.database_manager import DatabaseManager, DatabaseGame


@dataclass
class MatchmakingUser:
    account_id: int
    pref_rules: str
    pref_board_size: int
    callback: Callable[[Optional[int], int, int], None]


class Matchmaker:

    _singleton = None
    _lock: Lock = Lock()
    _users: List[MatchmakingUser] = []
    _pref_board_size: Optional[int] = None
    _match_lock: Lock = Lock()
    _db_complete_cv: Condition = Condition()
    _db_matchmaker_create_game_success: Optional[bool] = None
    _db_matchmaker_retrieve_game_success: Optional[bool] = None
    # _retrieved_dbg: Optional[DatabaseGame] = None
    _db_game_id: int = 0

    def __new__(cls, *args, **kwargs):
        """
        Ensures class remains a singleton.
        """
        if not cls._singleton:
            with cls._lock:
                cls._singleton = super(Matchmaker, cls).__new__(cls)
        return cls._singleton

    def match_user(
        self,
        account_id: int,
        rules: str,
        board_size: int,
        callback: Callable[[Optional[int], int, int], None],
    ) -> None:
        """
        Matches a user with another user with the same preference for rules and board size.
        If no match available immediately, user will be added to list of users looking for game so other users can
        match.

        :param account_id: ID of user who wants a match
        :param rules: Preferred game rules of user
        :param board_size: Preferred board size of user
        :param callback: Callback to call when match is successfully made
        """
        with self._match_lock:
            self._pref_board_size = board_size
            compatible_users: List[Tuple[int, MatchmakingUser]] = [
                (i, user)
                for i, user in enumerate(self._users)
                if user.pref_rules == rules and user.pref_board_size == board_size
            ]

            # If no users to match, add this user to list and return that no matches currently exist
            if len(compatible_users) == 0:
                self._users.append(
                    MatchmakingUser(
                        account_id=account_id,
                        pref_rules=rules,
                        pref_board_size=board_size,
                        callback=callback,
                    )
                )
                print("account_id: " + str(account_id))
                print("pref_rules: " + str(rules))
                print("pref_board_size: " + str(board_size))
                return None

            # If there are users to match, notify their callbacks
            pop_index, match_user = compatible_users[0]

        # Creating the game with matched user
        game_id: int = self._create_game(account_id, match_user.account_id, rules)
        print("after create_game game_id: " + str(game_id))
        print("after create_game self._db_game_id: " + str(self._db_game_id))

        match_user.callback(game_id, account_id, 2)
        callback(game_id, match_user.account_id, 1)

        with self._match_lock:
            # Remove matched user from users list
            self._users.pop(pop_index)

    def remove_user(self, account_id: int) -> None:
        """
        Removes a user from matchmaking consideration.

        :param account_id: Account ID of user to remove
        :return: True if all users with the same id is removed from the list; otherwise False
        """
        # Remove all users with the same ID as one provided (from back to front)
        with self._match_lock:
            reversed_users = reversed(self._users)
            for i, user in enumerate(reversed_users):
                if user.account_id == account_id:
                    self._users.pop(len(self._users) - 1 - i)

    def check_user_removed(self, account_id: int) -> bool:
        """

        :param account_id:
        :return: True if the user is not in the list anymore; False if the user is still in the waiting list
        """
        with self._match_lock:
            reversed_users = reversed(self._users)
            for i, user in enumerate(reversed_users):
                if user.account_id == account_id:
                    return False
            return True

    def _create_game(
        self, p1_account_id: int, p2_account_id: int, rule: str
    ) -> Optional[int]:
        """
        Create a game in the database with both online players' ids and their agreed game rule.

        :param p1_account_id: The account id for player 1 in the match
        :param p2_account_id:   The account id for player 2 in the match
        :param rule:            The rule that both player 1 and player 2 agree
        :return:                The game id for the one created; None if the game is not created successfully
        """
        # Add rule and account ids to DatabaseGame for creating game
        dbg: DatabaseGame = DatabaseGame(
            complete=False,
            board_state=self.__matchmaker_initialize_board(),
            rules=rule,
            next_turn=1,
            p1_account_id=p1_account_id,
            p2_account_id=p2_account_id,
            last_save=datetime.now(),
        )
        DatabaseManager().create_game(
            callback=self.__matchmaker_game_created_callback,
            database_game=dbg,
        )
        DatabaseManager().get_game(
            key=p1_account_id,
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

        print("in create_game: " + str(self._db_matchmaker_create_game_success))
        print("in create_game: " + str(self._db_matchmaker_retrieve_game_success))
        print("in create_game: " + str(self._db_game_id))
        if (
            self._db_matchmaker_create_game_success
            and self._db_matchmaker_retrieve_game_success
            and self._db_game_id != 0
        ):
            return self._db_game_id

        return None

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
                print("game_id in matchmaker: " + str(dbg.game_id))
            self._db_complete_cv.notify()

    def __matchmaker_initialize_board(self) -> [[int]]:
        size: int = self._pref_board_size
        cells: [[int]] = [[0] * size for _ in range(size)]
        # initialize the four starting disks at the center of the board
        cells[size // 2][size // 2 - 1] = 1
        cells[size // 2 - 1][size // 2] = 1
        cells[size // 2 - 1][size // 2 - 1] = 2
        cells[size // 2][size // 2] = 2
        return cells
