import datetime
import sys
from queue import Queue
from threading import Lock
from typing import Optional, Dict, Tuple, Callable, Any, NamedTuple, Union, List

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from server.config.config_reader import ConfigReader, DatabaseAccessInfo


class DatabaseConnectionException(Exception):
    pass


class DatabaseRequestInfo(NamedTuple):
    data: Any
    callback: Callable[..., None]


class DatabaseAccount(NamedTuple):
    account_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    elo: Optional[int] = None
    pref_board_length: Optional[int] = None
    pref_board_color: Optional[str] = None
    pref_disk_color: Optional[str] = None
    pref_opp_disk_color: Optional[str] = None
    pref_line_color: Optional[str] = None
    pref_rules: Optional[str] = None
    pref_tile_move_confirmation: Optional[bool] = None


class DatabaseGame(NamedTuple):
    game_id: Optional[int] = None
    complete: Optional[bool] = None
    board_state: Optional[List[List[int]]] = None
    rules: Optional[str] = None
    next_turn: Optional[int] = None
    p1_account_id: Optional[int] = None
    p2_account_id: Optional[int] = None
    ai_difficulty: Optional[int] = None
    last_save: Optional[datetime.datetime] = None


class DatabaseManager:

    _singleton = None
    _lock: Lock = Lock()

    _db_connection: Optional[MySQLConnection] = None
    _db_cursor: Optional[MySQLCursor] = None
    _queue: Queue = Queue()
    _cmd_dict: Dict[str, Callable[[DatabaseRequestInfo], None]] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            with cls._lock:
                if not cls._singleton:
                    cls._singleton = super(DatabaseManager, cls).__new__(cls)
                    cls._singleton._cmd_dict = {
                        "create_account": cls._singleton._create_account,
                        "delete_account": cls._singleton._delete_account,
                        "get_account": cls._singleton._get_account,
                        "update_account": cls._singleton._update_account,
                        "create_game": cls._singleton._create_game,
                        "delete_game": cls._singleton._delete_game,
                        "get_game": cls._singleton._get_game,
                        "update_game": cls._singleton._update_game,
                    }
        return cls._singleton

    def run(self) -> None:
        """
        Take the next command out of the queue and execute
        """
        next_cmd: str
        next_task_info: DatabaseRequestInfo
        next_cmd, next_task_info = self._queue.get()
        if next_cmd in self._cmd_dict:
            self._cmd_dict[next_cmd](next_task_info)

    def connect_database(self) -> None:
        """
        Connects to the database at the location given by a configuration file

        :raises DatabaseConnectionException: When the database can't be connected to.
            Top level doesn't need to know types of exceptions. Enough info is in error message
        """

        # First, get database info from config reader
        access_info: DatabaseAccessInfo = ConfigReader().get_database_access_info()
        if access_info is None:
            raise DatabaseConnectionException(f"Unknown database access info")

        try:
            # If trying to connect to a different database, make sure to close previous database connection first
            self.disconnect_database()
            # Connect to database server and start using correct database
            self._db_connection = mysql.connector.connect(
                host=access_info.host_ip,
                user=access_info.username,
                password=access_info.password,
            )
            self._db_cursor = self._db_connection.cursor()
            self._db_cursor.execute("use reversi")
        except Exception:
            raise DatabaseConnectionException(self._get_last_error())

    def disconnect_database(self) -> None:
        """
        Disconnects from the database that is currently connected, if any are connected

        :raises mysql.connection internal errors
        """
        if self._db_connection is not None:
            self._db_connection.close()

    def create_account(
        self,
        callback: Callable[[bool], None],
        database_account: DatabaseAccount,
    ) -> None:
        """
        Enqueues a create account command with the given user parameters

        :param callback: Callback to call when account creation is complete. True indicates success, false failure
        :param database_account: Info to create account with
        """
        self._enqueue(
            cmd="create_account",
            info=DatabaseRequestInfo(data=database_account, callback=callback),
        )

    def delete_account(self, callback: Callable[[bool], None], account_id: int) -> None:
        """
        Enqueues a create account command with the given user parameters

        :param callback: Callback to call when account deletion is complete. True indicates success, false failure
        :param account_id: ID of account to delete
        """
        self._enqueue(
            cmd="delete_account",
            info=DatabaseRequestInfo(data=account_id, callback=callback),
        )

    def get_account(
        self,
        callback: Callable[[bool, DatabaseAccount], None],
        key: Union[int, str],
        get_account_id: bool = False,
        get_username: bool = False,
        get_password: bool = False,
        get_elo: bool = False,
        get_pref_board_length: bool = False,
        get_pref_board_color: bool = False,
        get_pref_disk_color: bool = False,
        get_pref_opp_disk_color: bool = False,
        get_pref_line_color: bool = False,
        get_pref_rules: bool = False,
        get_pref_tile_move_confirmation: bool = False,
    ) -> None:
        """
        Queues request to get account info from the database

        :param callback: Callback to call on completion of account retrieval. True is success, false is failure.
        :param key: Account lookup key. Account ID for speed but can also be a username
        :param get_account_id: Whether to retrieve the account ID
        :param get_username: Whether to retrieve the username
        :param get_password: Whether to retrieve the password
        :param get_elo: Whether to retrieve the ELO
        :param get_pref_board_length: Whether to retrieve the board length preference
        :param get_pref_board_color: Whether to retrieve the board color preference
        :param get_pref_disk_color: Whether to retrieve the disk color preference
        :param get_pref_opp_disk_color: Whether to retrieve the opponent disk color preference
        :param get_pref_line_color: Whether to retrieve the line color preference
        :param get_pref_rules: Whether to retrieve the rules preference
        :param get_pref_tile_move_confirmation: Whether to retrieve tile move confirmation preference
        """
        data: Tuple[Any, ...] = (
            key,
            get_account_id,
            get_username,
            get_password,
            get_elo,
            get_pref_board_length,
            get_pref_board_color,
            get_pref_disk_color,
            get_pref_opp_disk_color,
            get_pref_line_color,
            get_pref_rules,
            get_pref_tile_move_confirmation,
        )
        self._enqueue(
            cmd="get_account", info=DatabaseRequestInfo(data=data, callback=callback)
        )

    def update_account(
        self,
        callback: Callable[[bool], None],
        account_id: int,
        database_account: DatabaseAccount,
    ) -> None:
        """
        Queues request to updates database account with given fields

        :param callback: Callback to call on completion of account update. True is success, false failure
        :param account_id: ID of account to update
        :param database_account: Info to change in account. All None fields will be ignored
        """
        data: Tuple[int, DatabaseAccount] = (account_id, database_account)
        self._enqueue(
            cmd="update_account", info=DatabaseRequestInfo(data=data, callback=callback)
        )

    def create_game(
        self,
        callback: Callable[[bool], None],
        database_game: DatabaseGame,
    ) -> None:
        """
        Enqueues a create game command with the given user parameters

        :param callback: Callback to call when game creation is complete. True indicates success, false failure
        :param database_game: Info to create game with
        """
        self._enqueue(
            cmd="create_game",
            info=DatabaseRequestInfo(data=database_game, callback=callback),
        )

    def delete_game(self, callback: Callable[[bool], None], game_id: int) -> None:
        """
        Enqueues a create game command with the given user parameters

        :param callback: Callback to call when account deletion is complete. True indicates success, false failure
        :param game_id: ID of game to delete
        """
        self._enqueue(
            cmd="delete_game",
            info=DatabaseRequestInfo(data=game_id, callback=callback),
        )

    def get_game(
        self,
        callback: Callable[[bool, DatabaseGame], None],
        key: int,
        last_game: bool = False,
        get_game_id: bool = False,
        get_complete: bool = False,
        get_board_state: bool = False,
        get_rules: bool = False,
        get_next_turn: bool = False,
        get_p1_account_id: bool = False,
        get_p2_account_id: bool = False,
        get_ai_difficulty: bool = False,
        get_last_save: bool = False,
    ) -> None:
        """
        Queues request to get game info from the database

        :param callback: Callback to call on completion of game retrieval. True is success, false is failure.
        :param key: ID of game to get (if not using last game) or account to get (if using last game)
        :param last_game: Whether to retrieve last game (true) or specific game (false)
        :param get_game_id: Whether to retrieve game ID
        :param get_complete: Whether to retrieve game completion
        :param get_board_state: Whether to retrieve board state
        :param get_rules: Whether to retrieve rules
        :param get_next_turn: Whether to retrieve next turn
        :param get_p1_account_id: Whether to retrieve player 1 account ID
        :param get_p2_account_id: Whether to retrieve player 2 account ID
        :param get_ai_difficulty: Whether to retrieve AI difficulty
        :param get_last_save: Whether to retrieve last save
        :return:
        """
        data: Tuple[Any, ...] = (
            key,
            last_game,
            get_game_id,
            get_complete,
            get_board_state,
            get_rules,
            get_next_turn,
            get_p1_account_id,
            get_p2_account_id,
            get_ai_difficulty,
            get_last_save,
        )
        self._enqueue(
            cmd="get_game", info=DatabaseRequestInfo(data=data, callback=callback)
        )

    def update_game(
        self,
        callback: Callable[[bool], None],
        game_id: int,
        database_game: DatabaseGame,
    ) -> None:
        """
        Queues request to updates database game with given fields

        :param callback: Callback to call on completion of game update. True is success, false failure
        :param game_id: ID of game to update
        :param database_game: Info to change in game. All None fields will be ignored
        """
        data: Tuple[int, DatabaseGame] = (game_id, database_game)
        self._enqueue(
            cmd="update_game", info=DatabaseRequestInfo(data=data, callback=callback)
        )

    def _create_account(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to insert new account into database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        acc: DatabaseAccount = request_info.data
        # Create new account with query
        query_str1: str = "insert into account ("
        query_str2: str = "values ("
        if acc.username is not None:
            query_str1 += "username,"
            query_str2 += f"'{acc.username}',"
        if acc.password is not None:
            query_str1 += "password,"
            query_str2 += f"'{acc.password}',"
        if acc.elo is not None:
            query_str1 += "elo,"
            query_str2 += f"{acc.elo},"
        if acc.pref_board_length is not None:
            query_str1 += "pref_board_length,"
            query_str2 += f"{acc.pref_board_length},"
        if acc.pref_board_color is not None:
            query_str1 += "pref_board_color,"
            query_str2 += f"'{acc.pref_board_color}',"
        if acc.pref_disk_color is not None:
            query_str1 += "pref_disk_color,"
            query_str2 += f"'{acc.pref_disk_color}',"
        if acc.pref_opp_disk_color is not None:
            query_str1 += "pref_opp_disk_color,"
            query_str2 += f"'{acc.pref_opp_disk_color}',"
        if acc.pref_line_color is not None:
            query_str1 += "pref_line_color,"
            query_str2 += f"'{acc.pref_line_color}',"
        if acc.pref_rules is not None:
            query_str1 += "pref_rules,"
            query_str2 += f"'{acc.pref_rules}',"
        if acc.pref_tile_move_confirmation is not None:
            query_str1 += "pref_tile_move_confirmation,"
            query_str2 += f"{int(acc.pref_tile_move_confirmation)},"
        query_str1 = query_str1[:-1]  # Remove last comma
        query_str2 = query_str2[:-1]  # Remove last comma
        query_str1 += ") "
        query_str2 += ")"
        query_str: str = query_str1 + query_str2
        success: bool = True
        try:
            self._db_cursor.execute(query_str)
            self._db_connection.commit()
        except Exception:
            success = False
        # Callback called with correct success boolean
        request_info.callback(success)

    def _delete_account(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to delete account from database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        account_id: int = request_info.data

        # Run query to delete account
        success: bool = True
        try:
            self._db_cursor.execute(
                f"delete from account where account_id = {account_id}"
            )
            self._db_connection.commit()
        except Exception:
            success = False
        # Callback called with correct success boolean
        request_info.callback(success)

    def _get_account(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to get account information from database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        key: Union[int, str]
        get_account_id: bool
        get_username: bool
        get_password: bool
        get_elo: bool
        get_pref_board_length: bool
        get_pref_board_color: bool
        get_pref_disk_color: bool
        get_pref_opp_disk_color: bool
        get_pref_line_color: bool
        get_pref_rules: bool
        get_pref_tile_move_confirmation: bool
        (
            key,
            get_account_id,
            get_username,
            get_password,
            get_elo,
            get_pref_board_length,
            get_pref_board_color,
            get_pref_disk_color,
            get_pref_opp_disk_color,
            get_pref_line_color,
            get_pref_rules,
            get_pref_tile_move_confirmation,
        ) = request_info.data

        # Check at least something is retrieved
        requested_fields: List[bool, ...] = [get for get in request_info.data[1:]]
        if not any(requested_fields):
            request_info.callback(False, DatabaseAccount())
            return

        # Run query to get account info
        success: bool = True
        query_str: str = (
            f"select "
            f"{'account_id,' if get_account_id else ''}"
            f"{'username,' if get_username else ''}"
            f"{'password,' if get_password else ''}"
            f"{'elo,' if get_elo else ''}"
            f"{'pref_board_length,' if get_pref_board_length else ''}"
            f"{'pref_board_color,' if get_pref_board_color else ''}"
            f"{'pref_disk_color,' if get_pref_disk_color else ''}"
            f"{'pref_opp_disk_color,' if get_pref_disk_color else ''}"
            f"{'pref_line_color,' if get_pref_line_color else ''}"
            f"{'pref_rules,' if get_pref_rules else ''}"
            f"{'pref_tile_move_confirmation,' if get_pref_tile_move_confirmation else ''}"
        )[
            :-1
        ]  # Remove last comma
        query_str += " from account where "
        query_str += (
            f"account_id = {key}" if type(key) == int else f"username = '{key}'"
        )
        dba: DatabaseAccount = DatabaseAccount()
        try:
            self._db_cursor.execute(query_str)
            # Grab result from query, make sure there's only 1 item (unique keys)
            raw_result: List[Tuple[Any, ...]] = self._db_cursor.fetchall()
            if len(raw_result) != 1:
                success = False
            else:
                # Transform query results to DatabaseAccount
                result: Tuple[Any] = raw_result[0]
                result_cnt: int = 0
                temp_dba: List[Any] = [None] * len(requested_fields)
                for i in range(len(requested_fields)):
                    if requested_fields[i]:
                        if i == dba._fields.index("pref_tile_move_confirmation"):
                            temp_dba[i] = bool(result[result_cnt])
                        else:
                            temp_dba[i] = result[result_cnt]
                        result_cnt += 1
                dba = DatabaseAccount(*temp_dba)
        except Exception:
            success = False
        # Callback called with correct success boolean and database account
        request_info.callback(success, dba)

    def _update_account(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to update account with given account info

        :param request_info: Additional info about request
        """
        # Extract data from request info
        account_id: int
        dba: DatabaseAccount
        account_id, dba = request_info.data

        # Run query to update account info
        query_str: str = "update account set "
        if dba.username is not None:
            query_str += f"username = '{dba.username}',"
        if dba.password is not None:
            query_str += f"password = '{dba.password}',"
        if dba.elo is not None:
            query_str += f"elo = {dba.elo},"
        if dba.pref_board_length is not None:
            query_str += f"pref_board_length = {dba.pref_board_length},"
        if dba.pref_board_color is not None:
            query_str += f"pref_board_color = '{dba.pref_board_color}',"
        if dba.pref_disk_color is not None:
            query_str += f"pref_disk_color = '{dba.pref_disk_color}',"
        if dba.pref_opp_disk_color is not None:
            query_str += f"pref_opp_disk_color = '{dba.pref_opp_disk_color}',"
        if dba.pref_line_color is not None:
            query_str += f"pref_line_color = '{dba.pref_line_color}',"
        if dba.pref_rules is not None:
            query_str += f"pref_rules = '{dba.pref_rules}',"
        if dba.pref_tile_move_confirmation is not None:
            query_str += (
                f"pref_tile_move_confirmation = {int(dba.pref_tile_move_confirmation)}"
            )
        query_str = query_str[:-1]  # Remove last comma
        query_str += f" where account_id = {account_id}"
        success: bool = True
        try:
            self._db_cursor.execute(query_str)
        except Exception:
            success = False
        # Callback called with correct success boolean and database account
        request_info.callback(success)

    def _create_game(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to insert new game into database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        game: DatabaseGame = request_info.data
        # Create new account with query
        query_args: List[Any] = []
        query_str1: str = "insert into game ("
        query_str2: str = "values ("
        if game.complete is not None:
            query_str1 += "complete,"
            query_str2 += f"{int(game.complete)},"
        if game.board_state is not None:
            query_str1 += "board_state,"
            query_str2 += "%s,"
            query_args.append(self.board_to_bytes(game.board_state))
        if game.rules is not None:
            query_str1 += "rules,"
            query_str2 += f"'{game.rules}',"
        if game.next_turn is not None:
            query_str1 += "next_turn,"
            query_str2 += f"{game.next_turn},"
        if game.p1_account_id is not None:
            query_str1 += "p1_account_id,"
            query_str2 += f"{game.p1_account_id},"
        if game.p2_account_id is not None:
            query_str1 += "p2_account_id,"
            query_str2 += f"{game.p2_account_id},"
        if game.ai_difficulty is not None:
            query_str1 += "ai_difficulty,"
            query_str2 += f"{game.ai_difficulty},"
        if game.last_save is not None:
            query_str1 += "last_save,"
            query_str2 += f"'{game.last_save.strftime('%Y-%m-%d %H:%M:%S')}',"
        query_str1 = query_str1[:-1]  # Remove last comma
        query_str2 = query_str2[:-1]  # Remove last comma
        query_str1 += ") "
        query_str2 += ")"
        query_str: str = query_str1 + query_str2
        success: bool = True
        try:
            self._db_cursor.execute(query_str, query_args)
            self._db_connection.commit()
        except Exception:
            success = False
        # Callback called with correct success boolean
        request_info.callback(success)

    def _delete_game(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to delete game from database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        game_id: int = request_info.data

        # Run query to delete account
        success: bool = True
        try:
            self._db_cursor.execute(f"delete from game where game_id = {game_id}")
            self._db_connection.commit()
        except Exception:
            success = False
        # Callback called with correct success boolean
        request_info.callback(success)

    def _get_game(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to get game information from database

        :param request_info: Additional info about request
        """
        # Extract data from request info
        key: int
        last_game: bool
        get_game_id: bool
        get_complete: bool
        get_board_state: bool
        get_rules: bool
        get_next_turn: bool
        get_p1_account_id: bool
        get_p2_account_id: bool
        get_ai_difficulty: bool
        get_last_save: bool
        (
            key,
            last_game,
            get_game_id,
            get_complete,
            get_board_state,
            get_rules,
            get_next_turn,
            get_p1_account_id,
            get_p2_account_id,
            get_ai_difficulty,
            get_last_save,
        ) = request_info.data

        # Check at least something is retrieved
        requested_fields: List[bool, ...] = [get for get in request_info.data[2:]]
        if not any(requested_fields):
            request_info.callback(False, DatabaseGame())
            return

        # Run query to get account info
        success: bool = True
        query_str: str = (
            f"select "
            f"{'game_id,' if get_game_id else ''}"
            f"{'complete,' if get_complete else ''}"
            f"{'board_state,' if get_board_state else ''}"
            f"{'rules,' if get_rules else ''}"
            f"{'next_turn,' if get_next_turn else ''}"
            f"{'p1_account_id,' if get_p1_account_id else ''}"
            f"{'p2_account_id,' if get_p2_account_id else ''}"
            f"{'ai_difficulty,' if get_ai_difficulty else ''}"
            f"{'last_save,' if get_last_save else ''}"
        )[
            :-1
        ]  # Remove last comma
        query_str += " from game "
        if last_game:
            query_str += f"where p1_account_id = {key} or p2_account_id = {key} order by last_save desc limit 1"
        else:
            query_str += f"where game_id = {key}"
        dbg: DatabaseGame = DatabaseGame()
        try:
            self._db_cursor.execute(query_str)
            # Grab result from query, make sure there's only 1 item (unique keys)
            raw_result: List[Tuple[Any, ...]] = self._db_cursor.fetchall()
            if len(raw_result) != 1:
                success = False
            else:
                # Transform query results to DatabaseGame
                result: Tuple[Any] = raw_result[0]
                result_cnt: int = 0
                temp_dbg: List[Any] = [None] * len(requested_fields)
                for i in range(len(requested_fields)):
                    if requested_fields[i]:
                        if i == dbg._fields.index("complete"):
                            temp_dbg[i] = bool(result[result_cnt])
                        elif i == dbg._fields.index("board_state"):
                            temp_dbg[i] = self.bytes_to_board(result[result_cnt])
                        else:
                            temp_dbg[i] = result[result_cnt]
                        result_cnt += 1
                dbg = DatabaseGame(*temp_dbg)
        except Exception:
            success = False
        # Callback called with correct success boolean and database game
        request_info.callback(success, dbg)

    def _update_game(self, request_info: DatabaseRequestInfo) -> None:
        """
        Create query to update game with given game info

        :param request_info: Additional info about request
        """
        # Extract data from request info
        game_id: int
        dbg: DatabaseGame
        game_id, dbg = request_info.data

        # Run query to update game info
        query_args: List[Any] = []
        query_str: str = "update game set "
        if dbg.complete is not None:
            query_str += f"complete = '{int(dbg.complete)}',"
        if dbg.board_state is not None:
            query_str += f"board_state = %s,"
            query_args.append(self.board_to_bytes(dbg.board_state))
        if dbg.rules is not None:
            query_str += f"rules = '{dbg.rules}',"
        if dbg.next_turn is not None:
            query_str += f"next_turn = {dbg.next_turn},"
        if dbg.p1_account_id is not None:
            query_str += f"p1_account_id = {dbg.p1_account_id},"
        if dbg.p2_account_id is not None:
            query_str += f"p2_account_id = {dbg.p2_account_id},"
        if dbg.ai_difficulty is not None:
            query_str += f"ai_difficulty = {dbg.ai_difficulty},"
        if dbg.last_save is not None:
            query_str += f"last_save = '{dbg.last_save.strftime('%Y-%m-%d %H:%M:%S')}',"
        query_str = query_str[:-1]  # Remove last comma
        query_str += f" where game_id = {game_id}"
        success: bool = True
        try:
            self._db_cursor.execute(query_str, query_args)
        except Exception:
            success = False
        # Callback called with correct success boolean and database account
        request_info.callback(success)

    def _enqueue(self, cmd: str, info: DatabaseRequestInfo) -> None:
        """
        Enqueues a command and database request info in one place so implementation can change freely

        :param cmd: Command as a string
        :param info: DatabaseRequestInfo that must be passed to an execution function
        """
        self._queue.put((cmd, info))

    @staticmethod
    def board_to_bytes(board: List[List[int]]) -> bytes:
        return bytes([cell for row in board for cell in row])

    @staticmethod
    def bytes_to_board(byte: bytes) -> List[List[int]]:
        flat_array: List[int] = [b for b in byte]
        board_size: float = len(flat_array) ** 0.5
        if not board_size.is_integer():
            raise ValueError(f"Inferred board length {board_size} not an integer")
        board_size: int = int(board_size)
        board_array: List[List[int]] = [
            [0 for _ in range(board_size)] for _ in range(board_size)
        ]
        for i in range(board_size):
            for j in range(board_size):
                board_array[i][j] = flat_array[i * board_size + j]
        return board_array

    @staticmethod
    def _get_last_error() -> str:
        return str(sys.exc_info()[0]) + "\n\t" + str(sys.exc_info()[1])
