from board import Board
from array_coord import array_to_coords

import numpy as np
from tkinter import *
from tkinter import messagebox


# FEATURE: rocks
# FEATURE: reveal all button

class Square(Button):

	"""Button that stores more information"""

	def __init__(self, master: object, row: int, col: int, **kwargs) -> None:
		super().__init__(master=master, **kwargs)
		self.row = row
		self.col = col
		self.clicked = False

		self.hit = False
		self.destroyed = False

	def get_coord(self) -> tuple:
		"""gets coordinate position of Square

		Returns:
			tuple: (row, col)
		"""

		return (self.row, self.col)

	def click(self) -> None:
		"""Square knows it has been cliked
		"""

		self.clicked = True

	def destroy(self) -> None:
		"""Square is part of a completely destroyed ship
		"""

		self.destroyed = True

	def attack(self) -> None:
		"""Square is part of a ship that has been hit
		"""

		self.hit = True

	def get_clicked(self) -> bool:
		"""Square click information

		Returns:
			bool: whether or not it has been clicked
		"""

		return self.clicked

	def get_destroyed(self) -> bool:
		"""Square destroyed information

		Returns:
			bool: whether or not it is part of a completely destroyed ship
		"""

		return self.destroyed


class BattleTabs(Frame):

	"""plays a game of Battle Tabs"""

	def __init__(self, master: Tk, rocks=[], sidelength=7) -> None:
		"""square grid in which players try to sink all enemy ships

		Args:
			master (Tk): root
			rocks (list, optional): list of unplayable Squares. Defaults to [].
			sidelength (int, optional): board dimensions. Defaults to 7.
		"""
		super().__init__(master)
		self.grid()

		self.root = master

		self.rocks = rocks
		self.sidelength = sidelength

		self.destroyed = 0

		self.board = Board(rocks, sidelength=sidelength)
		self.setup_buttons()

		# moves
		self.moves = 0
		self.move_counter = Label(self, text=str(self.moves), font=('Helvetica', 12))
		self.move_counter.grid(row=sidelength + 1, column=0, columnspan=4)

		# new game
		self.restart_button = Button(self, text='New Game', command=self.new_game)
		self.restart_button.grid(row=sidelength + 1, column=sidelength * 2 // 3, columnspan=4)

	def setup_buttons(self) -> None:
		"""creates an array of Squares and binds them to commands
		"""

		self.buttons = np.empty((self.sidelength, self.sidelength), dtype=Square)
		for row in range(self.sidelength):
			for col in range(self.sidelength):
				button = Square(self, row, col, width=4, height=2)

				button.config(command=lambda button=button: self.guess(button))
				button.bind('<Enter>', lambda event, button=button: self.hover(True, button, event))
				button.bind('<Leave>', lambda event, button=button: self.hover(False, button, event))

				self.buttons[row][col] = button

				self.buttons[row][col].grid(row=row + 1, column=col, rowspan=1, columnspan=1)

	def guess(self, button: Square) -> None:
		"""simulates a player guess

		Args:
			button (Square): Square that was guessed
		"""

		if (button.get_clicked()): # if it has already been guessed
			return

		self.move()
		button.click()
		self.hover(True, button, None)

		self.board.guess(coord := button.get_coord(), False)
		button.config(
			text=self.board.nearest_ship(coord),
			relief=SUNKEN,
			bg='grey'
			)

		if (type(self.board.output()[coord[0]][coord[1]]) != np.int32): # if a ship was hit
			button.attack()
			self.destroyed += 1
			for ship in self.board.ships:
				if (coord in (coords := [tuple(map(int, i)) for i in array_to_coords(ship.get_coords())])):
					[self.buttons[c[0]][c[1]].config(bg='red') for c in coords]
					[self.buttons[c[0]][c[1]].destroy() for c in coords]
					break
			if (self.destroyed == len(Board.ship_shapes)):
				again = messagebox.askyesno('You Win!', 'Congratulations! You Win!\nWould you like to play agin')
				self.new_game() if again else self.root.destroy()

	def new_game(self) -> None:
		"""starts a new game
		"""

		[button.destroy() for row in self.buttons for button in row]

		self.destroyed = 0
		self.moves = 0
		self.move_counter.config(text=str(self.moves))

		self.board = Board(self.rocks)
		self.setup_buttons()

	def move(self) -> None:
		"""increments move counter and updates display
		"""

		self.moves += 1
		self.move_counter.config(text=str(self.moves))

	def hover(self, hovering: bool, button: Square, _: Event) -> None:
		"""reveals information on hover

		Args:
			hovering (bool): entering or exiting button
			button (Square): Square that is being hovered over
			_ (Event): type of click
		"""

		if (not(button.get_clicked())):
			return

		coord = button.get_coord()
		color = 'light grey' if hovering else 'SystemButtonFace'
		secondary = color
		unknown = self.board.radius(self.board.nearest_ship(coord), coord)
		for coord in unknown:
			secondary = color
			if (self.buttons[coord[0]][coord[1]].get_clicked()): # if the button has already been clicked
				secondary = 'grey' # otherwise grey
				if (self.buttons[coord[0]][coord[1]].get_destroyed()): # if the coord is one of the destroyed ships
					secondary = 'red'

			self.buttons[coord[0]][coord[1]].config(bg=secondary)

root = Tk()
root.title('BattleTabs')
game = BattleTabs(root, sidelength=7)
game.mainloop()
