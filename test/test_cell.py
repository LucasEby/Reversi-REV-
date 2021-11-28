import unittest

from client.model.cell import Cell, CellState


class TestCell(unittest.TestCase):
    def test_flip(self):
        cell_1: Cell = Cell(CellState.player1)
        cell_1.flip()
        self.assertEqual(cell_1.state.value, 2)
        cell_2: Cell = Cell(CellState.player2)
        cell_2.flip()
        self.assertEqual(cell_2.state.value, 1)
        cell_e: Cell = Cell(CellState.empty)
        cell_e.flip()
        self.assertEqual(cell_e.state.value, 0)

    def test_fill(self):
        cell_1: Cell = Cell(CellState.player1)  # Cell(1)
        cell_1.fill(1)
        self.assertEqual(cell_1.state.value, 1)
        cell_1.fill(2)
        self.assertEqual(cell_1.state.value, 1)
        cell_2: Cell = Cell(CellState.player2)  # Cell(2)
        cell_2.fill(1)
        self.assertEqual(cell_2.state.value, 2)
        cell_2.fill(2)
        self.assertEqual(cell_2.state.value, 2)
        cell_e: Cell = Cell(CellState.empty)  # Cell(0)
        cell_e.fill(1)
        self.assertEqual(cell_e.state.value, 1)
        cell_e = Cell(CellState.empty)
        cell_e.fill(2)
        self.assertEqual(cell_e.state.value, 2)


if __name__ == "__main__":
    unittest.main()
