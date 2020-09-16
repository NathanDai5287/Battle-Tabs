import random

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

		self.setup_board()

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
