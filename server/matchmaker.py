from dataclasses import dataclass
from threading import Lock
from typing import List, Tuple, Callable


@dataclass
class MatchmakingUser:
    account_id: int
    pref_rules: str
    pref_board_size: int
    callback: Callable[[int], None]


class Matchmaker:

    _singleton = None
    _lock: Lock = Lock()
    _users: List[MatchmakingUser] = []
    _match_lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensures class remains a singleton
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
        callback: Callable[[int], None],
    ) -> None:
        """
        Matches a user with another user with the same preference for rules and board size.
        If no match available immediately, user will be added to list of users looking for game so other users can match.
        :param account_id: ID of user who wants a match
        :param rules: Preferred game rules of user
        :param board_size: Preferred board size of user
        :param callback: Callback to call when match is successfully made
        """
        with self._match_lock:
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
                return None

            # If there are users to match, notify their callbacks
            pop_index, match_user = compatible_users[0]
            match_user.callback(account_id)
            callback(match_user.account_id)
            # Remove matched user from users list
            self._users.pop(pop_index)

    def remove_user(self, account_id: int) -> None:
        """
        Removes a user from matchmaking consideration
        :param account_id: Account ID of user to remove
        """
        # Remove all users with the same ID as one provided (from back to front)
        with self._match_lock:
            reversed_users = reversed(self._users)
            for i, user in enumerate(reversed_users):
                if user.account_id == account_id:
                    self._users.pop(len(self._users) - 1 - i)
