import unittest

from cell import *


class TestCell(unittest.TestCase):
    def test_flip(self):
        cell = Cell.player1
        self.assertEqual(cell.flip(), 2)
        cell = Cell.player2
        self.assertEqual(cell.flip(), 1)
        cell = Cell.empty
        self.assertEqual(cell.flip(), 0)

    def test_fill(self):
        cell_1 = Cell.player1  # Cell(0)
        self.assertEqual(cell_1.fill(1), 1)
        self.assertEqual(cell_1.fill(2), 1)
        cell_2 = Cell.player2  # Cell(1)
        self.assertEqual(cell_2.fill(1), 2)
        self.assertEqual(cell_2.fill(2), 2)
        cell_e = Cell.empty  # Cell(2)
        self.assertEqual(cell_e.fill(1), 1)
        self.assertEqual(cell_e.fill(2), 2)


if __name__ == '__main__':
    unittest.main()
