import random
import numpy as np
from pprint import pformat

from ship import Ship
from array_coord import coord_to_array, array_to_coords


class Board:
	ship_shapes = [(1, 1), (2, 2), (1, 3), (1, 4)]

	def __init__(self, rocks=[], sidelength=7):
		"""initializes a BattleTabs Board

		Args:
				rocks (list, optional): list of rock coordinates. Defaults to [].
				sidelength (int, optional): board length. Defaults to 7.
		"""

		self.sidelength = sidelength
		self.rocks = rocks
		self.guesses = 0
		self.ships = []

		self.board = {}
		for row in range(sidelength):
			for col in range(sidelength):
				self.board[(row, col)] = False

		self.setup_board()

		self.nearest = np.empty((sidelength, sidelength), dtype=int)
		for row in range(sidelength):
			for col in range(sidelength):
				self.nearest[row][col] = self.nearest_ship((row, col))

		self.revealed = []
		self.completely_destroyed = []

	def __str__(self) -> str:
		reveal = [list(row) for row in self.nearest.copy()]
		for row in range(len(reveal)):
			for col in range(len(reveal)):
				coord = (row, col)
				if (coord not in self.revealed): # if ship is revealed
					reveal[row][col] = '~'

				if (coord in self.fully_destroyed()): # if the ship is fully destroyed
					ship = None

					for ship in self.ships: # find which ship this is
						if (coord in array_to_coords(ship.get_coords())):
							break # sets ship

					if (ship.shape == (1, 4) or ship.shape == (1, 3)): # if the ship is a 1 x 4 or 1 x 3
						if (ship.orientation % 2 == 1):
							reveal[row][col] = '|'
						else:
							reveal[row][col] = '-'
						
					else: # use *
						reveal[row][col] = '*'

		return pformat(reveal)

	def setup_board(self) -> None:
		"""changes self.board values to represent ships
		"""

		shuffled_ships = Board.ship_shapes.copy()
		random.shuffle(shuffled_ships)

		for dimension in shuffled_ships:
			ship = None
			placed = False
			while (not(placed)):
				coord = tuple([random.randint(0, self.sidelength) for _ in range(2)])
				orientation = random.randint(0, 3)
				ship = Ship(coord, orientation, dimension)
				placed = self.place(ship)
			self.ships.append(ship)

	def place(self, ship: Ship) -> bool:
		"""places a ship on the board

		Args:
			ship (Ship): contains coordinate, orientation, and dimensions

		Returns:
			bool: whether or not it placed successfully
		"""

		initial = self.board.copy()
		coords = ship.get_coords()
		if (not(ship.in_boundary())): # if the entire ship is on the board
			return False

		for coord in [tuple(arr) for arr in coords.transpose()]:
			if (self.board[coord]): # if the space is already taken
				self.board = initial.copy()
				return False
			self.board[coord] = True # place ship
		return True

	def nearest_ship(self, coord: tuple) -> int:
		"""finds the distance to the nearest ship on the board

		Args:
			coord (tuple): coordinate guessed

		Returns:
			int: distance
		"""

		if (self.board[coord]):
			return 0 # if a ship was hit

		hit_row, hit_col = coord
		max_distance = max(abs(hit_row - self.sidelength), abs(hit_col - self.sidelength), hit_row, hit_col)
		for distance in range(1, max_distance + 1):
			for row in range(-distance, distance + 1):
				col = distance - abs(row)

				scan_row = hit_row + row
				for i in [-1, 1]:
					scan_col = hit_col + col * i
					if (scan_row >= 0 and scan_row < self.sidelength and scan_col >= 0 and scan_col < self.sidelength): # check if in boundary
						if (self.board[(scan_row, scan_col)]):
							return abs(row) + abs(col)

		return False # board is empty

	def fully_destroyed(self) -> list:
		destroy_reveal = []
		for ship in self.ships:
			if (set(coords := array_to_coords(ship.get_coords())) <= set(self.revealed)):
				[destroy_reveal.append(coord) for coord in coords]
		return destroy_reveal

	def guess(self, coord):
		if (not(coord in self.revealed)):
			self.revealed.append(coord)
			self.guesses += 1

			print(self)

			return True
		return False
