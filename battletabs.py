from board import Board

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
				button = Square(self, row, col, width=2, height=1)
				button.config(command=lambda button=button: self.guess(button))
				self.buttons[row][col] = button

				self.buttons[row][col].grid(row=row + 1, column=col, rowspan=1, columnspan=1)

	def guess(self, button):
		valid = self.board.guess(coord := button.get_coord())
		button['text'] = self.board.nearest_ship(coord)

root = Tk()
root.title('BattleTabs')
game = BattleTabs(root)
game.mainloop()
