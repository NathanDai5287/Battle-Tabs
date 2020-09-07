from pprint import pformat
from typing import List, Tuple
import random
import numpy as np


class Ship:
	translations = [np.identity(2), np.array([[0, 1], [-1, 0]]), np.array([[-1, 0], [0, -1]]), np.array([[0, -1], [1, 0]])]
	def __init__(self, origin: np.ndarray, orientation: int, dimensions: tuple):
		self.ship_coord = np.array([(row, col) for row in range(dimensions[0]) for col in range(dimensions[1])])
		self.board_coord = np.matmul(Ship.translations[orientation], self.ship_coord) + origin

class Board:
	def __init__(self, rocks: List[Tuple], sidelength=7):
		self.board = [['~'] * sidelength] * sidelength
		self.rocks = rocks
		self.ships = [(1, 1), (2, 2), (1, 3), (1, 4)]

		for rock_coord in self.rocks:
			self.board[rock_coord[0]][rock_coord[1]] = 'X'
	
	def all_possible_placements(self):
		configurations = []
		for ship in [Ship(np.array([[row], [col]]), orientation, dimension)]:
			for row in range(self.sidelength):
				for col in range(self.sidelength):
					for orientation in range(4):
						for dimension in self.ships:
							

	def __str__(self):
		return pformat(self.board)

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(Ship.rotations(a))

"""
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 1 + 1 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
"""