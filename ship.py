import numpy as np

from array_coord import coord_to_array, array_to_coords

class Ship:
    translations = [np.identity(2), np.array([[0, 1], [-1, 0]]), np.array([[-1, 0], [0, -1]]), np.array([[0, -1], [1, 0]])]

    def __init__(self, origin: tuple, orientation: int, dimensions: tuple):
        """initializes a Ship

        Args:
                origin (tuple): where the ship will be placed
                orientation (int): number between 0 and 3
                dimensions (tuple): dimensions of ship
        """

        self.shape = dimensions
        self.orientation = orientation

        self.ship_coord = np.array([(row, col) for row in range(dimensions[0]) for col in range(dimensions[1])])
        self.board_coord = np.matmul(Ship.translations[orientation], self.ship_coord.transpose()) + np.array([[origin[0]], [origin[1]]]).astype(int)

    def get_coords(self):
        return self.board_coord

    def in_boundary(self, sidelength=7):
        return not(len(list(filter(lambda coord: coord[0] < 0 or coord[0] >= sidelength or coord[1] < 0 or coord[1] >= sidelength, array_to_coords(self.board_coord)))))
