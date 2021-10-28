import unittest

from client.model.board import Board
from client.model.cell import Cell, CellState


class TestBoard(unittest.TestCase):
    def test_input_validation(self):
        with self.assertRaises(Exception) as context:
            Board(7, 1)
        self.assertTrue("Board size must be an even number" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Board(6, 0)
        self.assertTrue(
            "Next turn must be a valid player (1 or 2)" in str(context.exception)
        )

    def test_init_cells(self):
        board_2 = Board(2, 1)
        self.assertEqual(board_2.cells[0][0], Cell.state.player2)
        self.assertEqual(board_2.cells[1][0], Cell.state.player1)
        self.assertEqual(board_2.cells[0][1], Cell.state.player1)
        self.assertEqual(board_2.cells[1][1], Cell.state.player2)
        board_4 = Board(4, 2)
        self.assertEqual(board_4.cells[0][0], Cell.state.empty)
        self.assertEqual(board_4.cells[0][3], Cell.state.empty)
        self.assertEqual(board_4.cells[3][0], Cell.state.empty)
        self.assertEqual(board_4.cells[3][3], Cell.state.empty)
        self.assertEqual(board_4.cells[1][1], Cell.state.player2)
        self.assertEqual(board_4.cells[1][2], Cell.state.player1)
        self.assertEqual(board_4.cells[2][1], Cell.state.player1)
        self.assertEqual(board_4.cells[2][2], Cell.state.player2)

    def test_get_state(self):
        cells_2 = [
            [Cell.state.player2, Cell.state.player1],
            [Cell.state.player1, Cell.state.player2],
        ]
        board_2 = Board(2, 1)
        self.assertEqual(board_2.get_state(), cells_2)
        cells_4 = [
            [Cell.state.empty, Cell.state.empty, Cell.state.empty, Cell.state.empty],
            [
                Cell.state.empty,
                Cell.state.player2,
                Cell.state.player1,
                Cell.state.empty,
            ],
            [
                Cell.state.empty,
                Cell.state.player1,
                Cell.state.player2,
                Cell.state.empty,
            ],
            [Cell.state.empty, Cell.state.empty, Cell.state.empty, Cell.state.empty],
        ]
        board_4 = Board(4, 2)
        self.assertEqual(board_4.get_state(), cells_4)

    def test_get_num_type(self):
        board_4 = Board(4, 1)  # has 16 cells: 2 - player1, 2 - player2, 12 - empty
        self.assertEqual(board_4.get_num_type(CellState.empty), 12)
        self.assertEqual(board_4.get_num_type(CellState.player1), 2)
        self.assertEqual(board_4.get_num_type(CellState.player2), 2)
        board_2 = Board(2, 1)  # has 4 cells: 2 - player1, 2 - player2, 0 - empty
        self.assertEqual(board_2.get_num_type(CellState.empty), 0)
        self.assertEqual(board_2.get_num_type(CellState.player1), 2)
        self.assertEqual(board_2.get_num_type(CellState.player2), 2)


if __name__ == "__main__":
    unittest.main()
