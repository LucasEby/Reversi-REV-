import unittest

from server.matchmaker import Matchmaker


class TestMatchmaker(unittest.TestCase):
    def test_match(self):
        match = Matchmaker().match_user(account_id=1, rules="standard", board_size=6)
        self.assertEqual(match, None)
        match = Matchmaker().match_user(account_id=2, rules="alternate", board_size=6)
        self.assertEqual(match, None)
        match = Matchmaker().match_user(account_id=3, rules="standard", board_size=8)
        self.assertEqual(match, None)
        match = Matchmaker().match_user(account_id=4, rules="alternate", board_size=8)
        self.assertEqual(match, None)
        match = Matchmaker().match_user(account_id=5, rules="standard", board_size=8)
        self.assertEqual(match, 3)
        match = Matchmaker().match_user(account_id=6, rules="standard", board_size=8)
        self.assertEqual(match, None)
        match = Matchmaker().match_user(account_id=7, rules="standard", board_size=6)
        self.assertEqual(match, 1)
        Matchmaker().remove_user(2)
        match = Matchmaker().match_user(account_id=8, rules="alternate", board_size=6)
        self.assertEqual(match, None)


if __name__ == '__main__':
    unittest.main()
