import unittest
import numpy as np

from board import Board
from ship import Ship

class Test(unittest.TestCase):
    def test_setup_board(self):
        """checks if the number of ships is correct
        """

        for test in range(10):
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

unittest.main()