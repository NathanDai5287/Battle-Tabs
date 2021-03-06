import unittest
import numpy as np

from board import Board
from ship import Ship


class Test(unittest.TestCase):
    def test_setup_board(self):
        """checks if the number of ships is correct
        """

        for _ in range(10):
            board = Board()

            temp_x, temp_y = map(max, zip(*board.board))
            res = np.array([[board.board.get((j, i), 0) for i in range(temp_y + 1)] for j in range(temp_x + 1)])
            ships = list(res.flatten()).count(True)

            self.assertEqual(ships, 12)

    def test_in_boundary(self):
        """test if the place method is correct
        """

        ship = Ship((5, 6), 0, (1, 4))
        self.assertFalse(ship.in_boundary())

        ship = Ship((6, 6), 0, (1, 1))
        self.assertTrue(ship.in_boundary())

        ship = Ship((0, 7), 2, (2, 2))
        self.assertFalse(ship.in_boundary())

    def test_nearest_ship(self):
        """tests the nearest_ship method
        """

        board = Board()
        board.board = np.array(
            [[False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, True, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False]]
        )

        nearest = board.nearest_ship((3, 3))
        self.assertEqual(nearest, 3)

        board.board = np.array(
            [[False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, True]]
        )

        nearest = board.nearest_ship((6, 6))
        self.assertEqual(nearest, 0)

        board.board = np.array(
            [[False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, True, True, False],
             [False, False, False, False, True, False, False],
             [False, False, False, False, False, False, False]]
        )

        nearest = board.nearest_ship((6, 6))
        self.assertEqual(nearest, 3)

        board.board = np.array(
            [[False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, True, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False]]
        )

        nearest = board.nearest_ship((6, 6))
        self.assertEqual(nearest, 4)

        board.board = np.array(
            [[False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, True, False, False],
             [False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False]]
        )

        nearest = board.nearest_ship((3, 1))
        self.assertEqual(nearest, 4)

    def test_game_over(self):
        """tests the game_over() methos
        """

        board = Board()
        for row in range(board.sidelength):
            for col in range(board.sidelength):
                board.guess((row, col))

        self.assertTrue(board.game_over())

        board = Board()
        for row in range(board.sidelength - 4):
            for col in range(board.sidelength - 4):
                board.guess((row, col))

        self.assertFalse(board.game_over())

        board = Board()

        for coord in [(row, col) for row in range(board.sidelength) for col in range(board.sidelength) if board.nearest[row][col] == 0]:
            board.guess(coord)

        self.assertTrue(board.game_over())
    
    def test_radius(self):
        coords = [(4, 4), (2, 4), (3, 1), (4, 2), (2, 2), (5, 3), (1, 3), (3, 5)]
        self.assertEqual(Board.radius(2, (3, 3)), coords)

        coords = [(1, 2), (2, 1), (0, 3), (3, 0)]
        self.assertEqual(Board.radius(3, (0, 0)), coords)

        coords = [(4, 0), (3, 1), (0, 2), (2, 2), (1, 3)]
        self.assertEqual(Board.radius(3, (1, 0)), coords)

        coords = [(5, 6), (6, 5)]
        self.assertEqual(Board.radius(1, (6, 6)), coords)

        coords = [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6), (6, 0)]
        self.assertEqual(Board.radius(6, (0, 0)), coords)

        coords = [(0, 0)]
        self.assertEqual(Board.radius(12, (6, 6)), coords)

unittest.main() # -b to suppress print
