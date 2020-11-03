from board import Board
from array_coord import array_to_coords

import numpy as np
from tkinter import *
from tkinter import messagebox


# FEATURE: check win
# FEATURE: new game
# FEATURE: move counter
# FEATURE: information on hover
# FEATURE: rocks
# FEATURE: reveal all button

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

		self.destroyed = 0
		self.moves = 0

		self.board = Board(rocks)
		self.setup_board()
	
	def setup_board(self):
		self.buttons = np.empty((self.sidelength, self.sidelength), dtype=Square)
		for row in range(self.sidelength):
			for col in range(self.sidelength):
				button = Square(self, row, col, width=4, height=2)
				button.config(command=lambda button=button: self.guess(button))
				self.buttons[row][col] = button

				self.buttons[row][col].grid(row=row + 1, column=col, rowspan=1, columnspan=1)

	def guess(self, button):
		if (button['relief'] == SUNKEN): # if it has already been guessed
			return

		self.board.guess(coord := button.get_coord())
		button.config(
			text=self.board.nearest_ship(coord), 
			relief=SUNKEN,
			bg='grey'
			)

		if (type(self.board.output()[coord[0]][coord[1]]) != np.int32):
			self.destroyed += 1
			for ship in self.board.ships:
				# breakpoint()
				if (coord in (coords := [tuple(map(int, i)) for i in array_to_coords(ship.get_coords())])):
					[self.buttons[c[0]][c[1]].config(bg='red') for c in coords]
					break
			self.new_game()

	def new_game(self):
		if (self.destroyed == len(Board.ship_shapes)):
			again = messagebox.askyesno('You Win!', 'Congratulations! You Win!\nWould you like to play agin')
			if (again):
				[button.destroy() for row in self.buttons for button in row]

				self.destroyed = 0
				self.moves = 0
				
				self.board = Board(self.rocks)
				self.setup_board()
			else:
				self.root.destroy()
			
root = Tk()
root.title('BattleTabs')
game = BattleTabs(root)
game.mainloop()
