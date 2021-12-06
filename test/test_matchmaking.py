import unittest
from typing import Dict, Any

from server.database_management.database_manager import (
    DatabaseManager,
    DatabaseAccount,
)


class TestMatchmaking(unittest.TestCase):
    def test_connection(self):
        # Create, connect and disconnect database with no errors
        DatabaseManager().connect_database()

        message1: Dict[str, Any] = {
            "protocol_type": "matchmaker",
            "my_account_id": 1,
            "pref_rule": "test_rule",
            "pref_board_size": 8,
        }

        message2: Dict[str, Any] = {
            "protocol_type": "matchmaker",
            "my_account_id": 2,
            "pref_rule": "test_rule",
            "pref_board_size": 8,
        }

        DatabaseManager().disconnect_database()
        # Ensure execution of query no longer works after disconnect
        with self.assertRaises(Exception):
            DatabaseManager()._db_cursor.execute("use reversi")
