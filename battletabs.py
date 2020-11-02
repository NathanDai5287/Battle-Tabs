from board import Board
from array_coord import array_to_coords

import numpy as np
from tkinter import *


class Square(Button):
	def __init__(self, master, row, col, clicked=False, **kwargs):
		super().__init__(master=master, **kwargs)
		self.row = row
		self.col = col
		self.clicked = clicked

	def get_coord(self):
		return (self.row, self.col)

	def get_clicked(self):
		return self.clicked

	def click(self):
		self.clicked = True

class BattleTabs(Frame):
	def __init__(self, master: Tk, rocks=[], sidelength=7):
		super().__init__(master)
		self.grid()

		self.root = master

		self.rocks = rocks
		self.sidelength = sidelength

		self.gameover = False
		self.moves = 0

		self.board = Board(rocks)

		self.buttons = np.empty((sidelength, sidelength), dtype=Square)
		for row in range(sidelength):
			for col in range(sidelength):
				button = Square(self, row, col, width=4, height=2)
				button.config(command=lambda button=button: self.guess(button))
				self.buttons[row][col] = button

				self.buttons[row][col].grid(row=row + 1, column=col, rowspan=1, columnspan=1)

	def guess(self, button):
		self.board.guess(coord := button.get_coord())
		button.config(
			text=self.board.nearest_ship(coord), 
			relief=SUNKEN,
			bg='grey'
			)

		if (type(self.board.output()[coord[0]][coord[1]]) != np.int32):
			for ship in self.board.ships:
				# breakpoint()
				if (coord in (coords := [tuple(map(int, i)) for i in array_to_coords(ship.get_coords())])):
					# [self.buttons[c[0]][c[1]].config(bg='red') for c in coords]
					for c in coords:
						self.buttons[c[0]][c[1]].config(bg='red')
					break

root = Tk()
root.title('BattleTabs')
game = BattleTabs(root)
game.mainloop()
