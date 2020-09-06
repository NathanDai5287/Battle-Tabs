from pprint import pformat


class Board:
    def __init__(self, sidelength, rocks, ships):
        
        self.board = [['~'] * sidelength] * sidelength
        self.ships = ships
        self.rocks = rocks

        for rock_coord in self.rocks:
            self.board[rock_coord[0]][rock_coord[1]] = 'X'

        
        
        # self.probability = [[100 / sidelength] * sidelength] * sidelength
        # self.rocks = rocks
        # self.total = sidelength * sidelength - len(rocks)

        # self.moves = [[None] * sidelength] * sidelength
        # for rock_coord in self.rocks:
        #     self.total -= 1
        #     self.probability[rock_coord[0]][rock_coord[1]] = 0


    def __str__(self):
        return pformat(self.board)

    @staticmethod
    def distance(self, row, col):
        return (row ** 2 + col ** 2)


    def guess(self, row, col):
        if ((row, col) in self.ships):
            self.board[row][col] = '0'
        else:



    
    """
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 1 + 1 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
    """