import datetime
import unittest
from unittest.mock import MagicMock

from server.database_management.database_manager import (
    DatabaseManager,
    DatabaseAccount,
    DatabaseGame,
)


class TestDatabaseManager(unittest.TestCase):
    def test_connection(self):
        # Create, connect and disconnect database with no errors
        DatabaseManager().connect_database()
        DatabaseManager().disconnect_database()
        # Ensure execution of query no longer works after disconnect
        with self.assertRaises(Exception):
            DatabaseManager()._db_cursor.execute("use reversi")

    def test_account(self):
        # Connect to database
        DatabaseManager().connect_database()

        # Create account function with no errors, ensuring callback was called successfully
        create_account_request_data = DatabaseAccount(
            None,
            "username",
            "password",
            0,
            8,
            "board_color",
            "disk_color",
            "opp_disk_color",
            "line_color",
            "rules",
            False,
        )
        callback = MagicMock()
        DatabaseManager().create_account(callback, create_account_request_data)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        # Get account info and test it is all correct
        get_account_request_data = (
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        )
        callback.reset_mock()
        DatabaseManager().get_account(callback, "username", *get_account_request_data)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(
            True, DatabaseAccount(*create_account_request_data)
        )

        # Get account ID
        callback.reset_mock()
        DatabaseManager().get_account(
            callback=callback, key="username", get_account_id=True
        )
        DatabaseManager().run(run_once=True)
        account_id: int = callback.call_args[0][1].account_id

        # Get account info via account ID and verify it is all correct
        callback.reset_mock()
        DatabaseManager().get_account(callback, account_id, *get_account_request_data)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(
            True, DatabaseAccount(*create_account_request_data)
        )

        # Update an account field and test it was updated
        callback.reset_mock()
        DatabaseManager().update_account(
            callback=callback,
            account_id=account_id,
            database_account=DatabaseAccount(
                password="password2", pref_rules="weird_rules"
            ),
        )
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        callback.reset_mock()
        DatabaseManager().get_account(
            callback=callback,
            key=account_id,
            get_username=True,
            get_password=True,
            get_pref_rules=True,
        )
        DatabaseManager().run(run_once=True)
        dba: DatabaseAccount = callback.call_args[0][1]
        self.assertEqual("username", dba.username)
        self.assertEqual("password2", dba.password)
        self.assertEqual("weird_rules", dba.pref_rules)

        # Delete account and ensure it can no longer be retrieved
        callback.reset_mock()
        DatabaseManager().delete_account(callback=callback, account_id=account_id)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        callback.reset_mock()
        DatabaseManager().get_account(
            callback=callback, key=account_id, get_account_id=True
        )
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(False, DatabaseAccount())

        # Disconnect from database
        DatabaseManager().disconnect_database()

    def test_game(self):
        # Connect to database
        DatabaseManager().connect_database()

        # Create account and get account ID so new game can reference it
        create_account_request_data = DatabaseAccount(
            None,
            "username",
            "password",
            0,
            8,
            "board_color",
            "disk_color",
            "opp_disk_color",
            "line_color",
            "rules",
            False,
        )
        callback = MagicMock()
        DatabaseManager().create_account(callback, create_account_request_data)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)
        callback.reset_mock()
        DatabaseManager().get_account(
            callback=callback, key="username", get_account_id=True
        )
        DatabaseManager().run(run_once=True)
        account_id: int = callback.call_args[0][1].account_id

        # Create game function with no errors
        dbg: DatabaseGame = DatabaseGame(
            None,
            False,
            [[1, 2], [2, 1]],
            "standard",
            1,
            account_id,
            None,
            None,
            datetime.datetime.strptime("11-01-2021 03:00:00", "%m-%d-%Y %H:%M:%S"),
        )
        callback.reset_mock()
        DatabaseManager().create_game(callback=callback, database_game=dbg)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        # Create second (more recent) game with same account as P2
        dbg2: DatabaseGame = DatabaseGame(
            None,
            False,
            [[1, 2], [2, 1]],
            "standard",
            1,
            None,
            account_id,
            None,
            datetime.datetime.strptime("11-02-2021 03:00:00", "%m-%d-%Y %H:%M:%S"),
        )
        callback.reset_mock()
        DatabaseManager().create_game(callback=callback, database_game=dbg2)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        # Get last game and ensure it matches second game
        get_game_request_data = (
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        )
        callback.reset_mock()
        DatabaseManager().get_game(callback, account_id, True, *get_game_request_data)
        DatabaseManager().run(run_once=True)
        game_id: int = callback.call_args[0][1].game_id
        dbg_check = dbg2._replace(game_id=game_id)
        callback.assert_called_once_with(True, dbg_check)

        # Get second-to-last game and ensure it matches first game
        callback.reset_mock()
        DatabaseManager().get_game(callback, game_id - 1, False, *get_game_request_data)
        DatabaseManager().run(run_once=True)
        dbg_check = dbg._replace(game_id=game_id - 1)
        callback.assert_called_once_with(True, dbg_check)

        # Update game and check updates occurred
        callback.reset_mock()
        DatabaseManager().update_game(
            callback=callback,
            game_id=game_id,
            database_game=DatabaseGame(complete=True, next_turn=2),
        )
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        callback.reset_mock()
        DatabaseManager().get_game(
            callback=callback,
            key=game_id,
            last_game=False,
            get_game_id=True,
            get_complete=True,
            get_next_turn=True,
        )
        DatabaseManager().run(run_once=True)
        dbg: DatabaseGame = callback.call_args[0][1]
        self.assertEqual(game_id, dbg.game_id)
        self.assertEqual(True, dbg.complete)
        self.assertEqual(2, dbg.next_turn)

        # Delete games
        callback.reset_mock()
        DatabaseManager().delete_game(callback=callback, game_id=game_id)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)
        callback.reset_mock()
        DatabaseManager().delete_game(callback=callback, game_id=game_id - 1)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        # Delete account
        callback.reset_mock()
        DatabaseManager().delete_account(callback=callback, account_id=account_id)
        DatabaseManager().run(run_once=True)
        callback.assert_called_once_with(True)

        # Disconnect from database
        DatabaseManager().disconnect_database()


if __name__ == "__main__":
    unittest.main()
