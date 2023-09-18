# This file contain a functions used by the level widgets

import tkinter as tk

from .settings import MENU_FONT

class Level:
	def __init__(self, master=None):
		self.master = master
		self.GAME_LEVEL = 1
		self.CURRENT_LEVEL = 1

	def create_levels(self, master, length: int, widget_to_close=None) -> None:
		"""This function creates level button in the canvas widget
			:param:master-> tkinter frame widget
		"""
		global MENU_FONT
		length = length
		
		count = 1
		state = tk.NORMAL
		common_style = {"width": 7, "padx": 5, "height": 3, "justify": tk.CENTER,
		"relief": tk.GROOVE, "font": MENU_FONT}
		for row in range(1, length+1):
			for column in range(1, length+1):
				if count > self.GAME_LEVEL:
					state = tk.DISABLED
				button = self.tk_button(master, count, state, **common_style)
				button.grid(row=row, column=column, sticky=tk.NSEW)

				if count == 9:
					return

				count += 1

	def increase_game_level(self):
		""" Function for increasing Game Level"""
		if self.GAME_LEVEL == 10:
			self.GAME_LEVEL = 10
			return
		elif self.CURRENT_LEVEL == self.GAME_LEVEL:
			self.GAME_LEVEL += 1

	def move_to_next_level(self):
		"""Method used to move to next level"""
		if self.CURRENT_LEVEL < self.GAME_LEVEL and self.CURRENT_LEVEL < 9:
			self.CURRENT_LEVEL += 1

		level = self.CURRENT_LEVEL + 1
		return level

	def on_button_click(self, level):
		"""After the button clicked player enter to the certain level which are available,
			to play
		"""
		if level <= self.GAME_LEVEL:
			self.CURRENT_LEVEL = level

		self.master.on_level_button_click(level=self.CURRENT_LEVEL + 1)

	def tk_button(self, master: object, count: int, state: str, **kw):
		# Tkinter drawback of creating buttons
		"""To know this method better see the self.create_level method"""
		button = tk.Button(master, text=str(count), command=lambda: self.on_button_click(count),
					state=state, **kw)

		return button