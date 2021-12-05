import unittest
from typing import Tuple, List

from client.model.calculate_new_elos import CalculateNewELOs


class TestCalculateNewELOs(unittest.TestCase):
    calc = CalculateNewELOs()

    def test_worse_player_won(self):
        p1_id: int = 1
        p1_elo: int = 200
        p2_id: int = 2
        p2_elo: int = 250
        p1_won: bool = True
        new_elos: List[Tuple[int, int]] = self.calc.get_new_elos(
            p1_id, p1_elo, p2_id, p2_elo, p1_won
        )
        self.assertEqual(new_elos[0], (1, 213))
        self.assertEqual(new_elos[1], (2, 237))

    def test_better_player_won(self):
        p1_id: int = 1
        p1_elo: int = 200
        p2_id: int = 2
        p2_elo: int = 300
        p1_won: bool = False
        new_elos: List[Tuple[int, int]] = self.calc.get_new_elos(
            p1_id, p1_elo, p2_id, p2_elo, p1_won
        )
        self.assertEqual(new_elos[0], (1, 180))
        self.assertEqual(new_elos[1], (2, 320))

    def test_players_with_same_elo(self):
        p1_id: int = 1
        p1_elo: int = 250
        p2_id: int = 2
        p2_elo: int = 250
        p1_won: bool = True
        new_elos: List[Tuple[int, int]] = self.calc.get_new_elos(
            p1_id, p1_elo, p2_id, p2_elo, p1_won
        )
        self.assertEqual(new_elos[0], (1, 266))
        self.assertEqual(new_elos[1], (2, 234))


if __name__ == "__main__":
    unittest.main()
