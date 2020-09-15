import random
import numpy as np

from ship import Ship


class Board:
	def __init__(self, rocks=[], sidelength=7):
		"""initializes a BattleTabs Board

		Args:
				rocks (list, optional): list of rock coordinates. Defaults to [].
				sidelength (int, optional): board length. Defaults to 7.
		"""

		self.sidelength = sidelength
		self.board = {}
		self.rocks = rocks
		self.ship_shapes = [(1, 1), (2, 2), (1, 3), (1, 4)]

		for row in range(sidelength):
			for col in range(sidelength):
				self.board[(row, col)] = False

		for rock_coord in self.rocks:
			self.board[rock_coord] = None

		self.setup_board()

	@staticmethod
	def array_to_coord(array: np.ndarray) -> tuple:
		"""converts an array to tuple form

		Args:
			array (np.ndarray): [[x], [y]]

		Returns:
			tuple: (x, y)
		"""

		return tuple(array.flatten())

	def setup_board(self) -> None:
		"""changes self.board values to represent ships
		"""

		shuffled_ships = self.ship_shapes.copy()
		random.shuffle(shuffled_ships)
		for dimension in shuffled_ships:
			placed = False
			while (not(placed)):
				coord = tuple([random.randint(0, self.sidelength) for _ in range(2)])
				orientation = random.randint(0, 3)
				ship = Ship(coord, orientation, dimension)
				placed = self.place(ship)

	def place(self, ship: Ship) -> bool:
		"""places a ship on the board

		Args:
			ship (Ship): contains coordinate, orientation, and dimensions

		Returns:
			bool: whether or not it placed successfully
		"""

		initial = self.board.copy()
		coords = ship.get_coords()
		if (not(ship.in_boundary())):
			return False
		for coord in [tuple(arr) for arr in coords.transpose()]:
			if (self.board[coord]):
				self.board = initial.copy()
				return False
			self.board[coord] = True
		return True
