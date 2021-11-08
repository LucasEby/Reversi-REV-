import sys
from queue import Queue
from typing import Optional, Dict, Tuple, Callable, NamedTuple, Any

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from server.config.config_reader import ConfigReader, DatabaseAccessInfo


class DatabaseConnectionException(Exception):
    pass


class DatabaseRequest(NamedTuple):
    data: Any
    callback: Callable[[Any], None]


class DatabaseManager:

    def __init__(self) -> None:
        """
        Database Manager for communication with a mySQL database
        """
        self._db_connection: Optional[MySQLConnection] = None
        self._db_cursor: Optional[MySQLCursor] = None
        self._queue: Queue = Queue()
        self._cmd_dict: Dict[str, Callable[[DatabaseRequest], None]] = {

        }

    def run(self) -> None:
        cmd: str = self._queue.get()
        if cmd in self._cmd_dict:
            self._cmd_dict[cmd]()

    def _connect_database(self) -> None:
        """
        Connects to the database at the location given by a configuration file

        :raises DatabaseConnectionException: When the database can't be connected to.
            Top level doesn't need to know types of exceptions. Enough info is in error message
        """

        # First, get database info from config reader
        access_info: DatabaseAccessInfo = (
            ConfigReader.get_instance().get_database_access_info()
        )
        if access_info is None:
            raise DatabaseConnectionException(f"Unknown database access info")

        try:
            # If trying to connect to a different database, make sure to close previous database connection first
            self._disconnect_database()
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

    def _disconnect_database(self) -> None:
        """
        Disconnects from the database that is currently connected, if any are connected

        :raises mysql.connection internal errors
        """
        if self._db_connection is not None:
            self._db_connection.close()

    @staticmethod
    def _get_last_error():
        return str(sys.exc_info()[0]) + "\n\t" + str(sys.exc_info()[1])

