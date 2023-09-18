""":about:This is the main python file of the game "SlidePuzzle". Which is actually a puzzle based game,
		Where you should matched a sequence of number accordingly to further incresing the levels. This
		project is made just for seeking potential of the tkinter module in game development.
			Where ever tkinter lack to provide functionality I use other module. For playing sound I use
		Arcade Module(a 2d game development module in python)

	:author: Ramayan Marid
	:email: ramayanmardi@gmail.com
	:lisence: free to use for any purpose and modifiable
	
	:python version: Python 3.11.1
	:tkinter version: `Tkinter module used which comes with the bundle of "python version-3.11.1"`
	:os version: Used for file handling purpose(come with the bundle of "python version-3.11.1")
	:random version: Used for randamizaton(come with the bundle of "python version-3.11.1")
	--------------> Other modules used in this game <-------------------------------
	:Arcade version: Arcade 2.6.17
	--------------> Used components used in this game <----------------------------
	component.settings.py -> here all the settings related variable are present for the game.
	component.logic.py -> all logic for the game to work.
	component.gui.py -> Gui related staff (Main Menu Gui etc.)
	component.level_logic.py -> logic for the levels.
	component.pop_up.py -> handels the pop_up gui in the game.
	componet.gui_player.py -> handels the gui played the game.

	Note: `For running the game ensure that you install all the necessary dependencies and all the file,
		are in the appropriate directories`
"""

"""
	Note: When creating an image in tkinter on the canvas widget and moving the image using the
		position attribute of the canvas widget, it is important to note that the image is not moved
		based on the top-left corner like in many other game engines. Instead, it is moved based on the
		middle position of the image.
"""

# (To know this below line better read the the SlidePuzzle class method global_bind_key, bind_gui_key)
# WIDGET NAME FOR THE GAME WHICH IS USED: (GUI, GAME, WINSCREEN, LOSSSCREEN, SETTING, ABOUT,

# EXTAR...
"""
Symbol booked by the programme
"$" : as seperator in about widget
"~" : as seperator in about widget
-------------
Special Sequence that are reserve for game for internal use: --->
Control+Alt+KeyPress+F1: for calling addguibinding
Control+Alt+KeyPress+F2: for calling unbindguibinding
"""

import tkinter as tk
from tkinter import ttk
import os
import random as rand

# Importing local modules
from component.settings import *
from component.logic import *
from component.gui import Gui
from component.level_logic import Level
from component.pop_up import PopUp
from component.gif_player import GIF_PLAYER

# Images Used in the game
Image_for_game = ["back.png", "play_again.png", "cheat.png", "shuffle.png", "arrow_right.png"]

class PreparingWindow(tk.Tk):
	"""This is the class preparing game window. Here you can control the window of the game"""
	def __init__(self, **kw):
		super().__init__(**kw)	
		self.wm_title("SlidePuzzle")
		SCREEN_SIZE = (self.winfo_screenwidth(), self.winfo_screenheight())
		center_x = (SCREEN_SIZE[0] - WINDOW_SIZE[0])//2
		center_y =  (SCREEN_SIZE[1] - WINDOW_SIZE[1])//2
		self.wm_geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{center_x}+{center_y}")
		self.wm_resizable(width=False, height=False)
		self.wm_attributes("-topmost", True)
		self.wm_iconbitmap(bitmap=icon_dir+"/slidepuzzle.ico")

		
		
class SlidePuzzle(tk.Frame):
	"""This is one of the important class of this game. Here I am combining all the other module,
		as well as logic for the game.

		:param master: `root`\'`master` of tkinter module (object of `tkinter.Tk()`)

		For creating the class you only need to provide the the `master`. If you want to modifie the class
		variables or properties pass the arguments as `kwargs` formate {*{dict}} 
	"""
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		# ------ Variables for game -----------
		self.main_parent = master # Parent of all the widget
		try:
			# extracting all the essential data, by calling necessary functions
			self.puzzle_data, self.slidepuzzle_length, self.slidepuzzle_size = load_slidepuzzlenum(2)
			self.GLOBAL_PUZZLE_DATA = self.puzzle_data.copy() # this copied data used as a global variable
			self.game_image = load_image_and_return_dict(icon_dir, Image_for_game)
			
			# I found one lack during using the 'arcade module' as a music player, it can't play sound in time
			# if, we can't use this type of code befor actually using that module as a music player.
			mymusicplayer.set_volume(0.0)
			mymusicplayer.play_audio(BUTTON_SOUND_1)
			mymusicplayer.set_volume(0.6)
		except ValueError:
			print("Data not loaded accurately..")
			# In-built method tkinter to quit the Tcl methods and destroy all the widgets.
			self.quit()

		# Variable do works as their name
		self.GAME_VOLUME_LEVEL = tk.IntVar()
		self.GAME_VOLUME_LEVEL.set(60)
		self.LevelClass = Level(self)

		self.GifPlayer = GIF_PLAYER(self.main_parent)


		# Main frame all game releted object should lies in this frame
		self.main_game_frame = tk.Frame(self) # Frame for holding game
		self.gui_frame = tk.Frame(self) # Frame for holding gui
		self.gui_frame.pack(fill=tk.BOTH)

		Gui(self.gui_frame, relief=tk.SOLID, height=WINDOW_SIZE[1]).pack(fill=tk.BOTH)
		self.global_bind_key()
		self.bind_gui_key()
		self.game_canvas = tk.Canvas(self.main_game_frame)

	def run_game(self, event=None):
		"""Method that able to run the game"""
		global UNBINDING_WIDGET_NAME, GAME_FONT_NAME

		self.gui_frame.pack_forget()
		# TODO: This data needed to be more costomizable.
		UNBINDING_WIDGET_NAME = "GUI"
		self.master.event_generate("<<UNBINDGUIBINDING>>")
		# Starting game code --------------->

		# Handling Packing of the widget -------->
		self.main_game_frame.pack(fill=tk.BOTH)
		self.main_game_frame_pack_info = self.main_game_frame.pack_info()
		self.game_canvas.pack(fill=tk.BOTH, side=tk.TOP)		

		rand.shuffle(self.puzzle_data)
		# Level pop-up would occure by the below code when game runs
		level_message = "Level:- " + str(self.LevelClass.CURRENT_LEVEL)
		PopUp(self.main_parent, level_message)
		
		self.slidepuzzle_look()
		self.shuffle_button()
		self.bind_key() # Binding Game Widget Key

	def slidepuzzle_look(self):
		length = self.slidepuzzle_length
		size_of_tile = self.slidepuzzle_size

		pos = [10, 10]
		count = 0
		for y in range(1, length+1):
			for x in range(1, length+1):
				self.game_canvas.create_rectangle((pos[0], pos[1], pos[0]+size_of_tile, pos[1]+size_of_tile),
					fill=self.puzzle_data[count]["color"])
				self.game_canvas.create_text((pos[0] + (size_of_tile//2), pos[1] + (size_of_tile//2)),
					text=self.puzzle_data[count]["num"], font=MENU_FONT)
				# TODO:- FIND THE SOLUTION WHY THE IMAGE IS NOT LOADING IN CANVAS ------------->
				# tkinter_image = tk.PhotoImage(file=self.puzzle_data[count]["image"])
				# self.game_canvas.create_image((100, 100), image=tkinter_image)
				
				pos[0] = (size_of_tile * x) + 10
				count += 1

			pos[1] = (size_of_tile * y) + 10
			pos[0] = 10

	def bind_gui_key(self, event=None):
		"""Binding method for GUI widget """
		global UNBINDING_WIDGET_NAME

		UNBINDING_WIDGET_NAME = "GAME"
		self.unbind_all_key() # TODO: FIND SOLUTION WHY EVENT IS NOT GENERATED HERE
		make_id_for_unbind("GUI", "<KeyPress-n>", self.master.bind("<KeyPress-n>", self.run_game))
		
	def unbind_all_key(self, event=None):
		global UNBINDING_WIDGET_NUMBER, UNBINDING_WIDGET_NAME, WIDGET_SEQ_AND_FUNCID

		Key_to_be_deleted = []
		if UNBINDING_WIDGET_NAME or UNBINDING_WIDGET_NUMBER:
			for key in WIDGET_SEQ_AND_FUNCID.keys():
				if UNBINDING_WIDGET_NUMBER and UNBINDING_WIDGET_NAME:
					if key.split("_")[0] == UNBINDING_WIDGET_NAME + "_" + set(UNBINDING_WIDGET_NUMBER):
						self.master.unbind(WIDGET_SEQ_AND_FUNCID[key][0], WIDGET_SEQ_AND_FUNCID[key][1])
						Key_to_be_deleted.append(key)
				elif UNBINDING_WIDGET_NAME:
					if key.split("_")[0] == UNBINDING_WIDGET_NAME:
						self.master.unbind(WIDGET_SEQ_AND_FUNCID[key][0], WIDGET_SEQ_AND_FUNCID[key][1])
						Key_to_be_deleted.append(key)
			# Clear key_id which are unbind --------->
			if Key_to_be_deleted:
				for key in Key_to_be_deleted:
					WIDGET_SEQ_AND_FUNCID.pop(key)

		UNBINDING_WIDGET_NAME, UNBINDING_WIDGET_NUMBER = None, None

	def set(self, unbinding_widget_name: str = None, unbinding_widget_number: int = None):
		"""setter function for the variable used by different class"""
		global UNBINDING_WIDGET_NAME, UNBINDING_WIDGET_NUMBER

		UNBINDING_WIDGET_NAME, UNBINDING_WIDGET_NUMBER = unbinding_widget_name, unbinding_widget_number

	def global_bind_key(self):
		self.master.bind("<KeyPress-q>", self.logic)
		# Adding Events --->
		self.master.event_add("<<ADDGUIBINDING>>", "<Control-Alt-KeyPress-F1>")
		self.master.event_add("<<UNBINDGUIBINDING>>", "<Control-Alt-KeyPress-F2>")

		# Controls Volume event
		self.master.bind("<KeyPress-e>", lambda *args: self.increase_game_volume(self.GAME_VOLUME_LEVEL, 10, "+"))
		self.master.bind("<KeyPress-r>", lambda *args: self.increase_game_volume(self.GAME_VOLUME_LEVEL, 10, "-"))

		# Constom binding ------------>
		self.master.bind("<<ADDGUIBINDING>>", self.bind_gui_key)
		self.master.bind("<<UNBINDGUIBINDING>>", self.unbind_all_key)

	def bind_key(self):
		# --------- KEYBOAD KEY -------------
		make_id_for_unbind("GAME", "<KeyPress-w>", self.master.bind("<KeyPress-w>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-a>", self.master.bind("<KeyPress-a>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-s>", self.master.bind("<KeyPress-s>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-d>", self.master.bind("<KeyPress-d>", self.logic))

		# ----------- ARROW BUTTON --------------
		make_id_for_unbind("GAME", "<KeyPress-Left>", self.master.bind("<KeyPress-Left>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-Right>", self.master.bind("<KeyPress-Right>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-Up>", self.master.bind("<KeyPress-Up>", self.logic))
		make_id_for_unbind("GAME", "<KeyPress-Down>", self.master.bind("<KeyPress-Down>", self.logic))
		
		# ------------- BINDING OTHERS BUTTON (CHEAT, SHUFFLE) ----------
		make_id_for_unbind("GAME", "<KeyPress-c>", self.master.bind("<KeyPress-c>", self.cheat))
		make_id_for_unbind("GAME", "<KeyPress-v>", self.master.bind("<KeyPress-v>", self.create_new_game))

	def logic(self, event):
		"""Logic for the game"""
		blank_index = get_index(data=self.puzzle_data) # Get the index number of blank digit
		length_of_puzzle_data = len(self.puzzle_data) - 1
		resticted_number_right = creating_restricted_loacation_right(self.slidepuzzle_length)
		resticted_number_left = creating_restricted_loacation_left(self.slidepuzzle_length)
		new_index = 0

		# Checking all the possible inputs may possible
		if event.char == "s" or event.keysym == "Down":
			new_index = blank_index - self.slidepuzzle_length
			if new_index >= 0:
				mymusicplayer.play_audio(TILE_SOUND)
				self.puzzle_data = swife_element(self.puzzle_data, with_=get_num(self.puzzle_data, new_index))
			else:
				mymusicplayer.play_audio(WRONG_SOUND)
		elif event.char == "w" or event.keysym == "Up":
			new_index = blank_index + self.slidepuzzle_length
			if new_index <= length_of_puzzle_data:
				mymusicplayer.play_audio(TILE_SOUND)
				self.puzzle_data = swife_element(self.puzzle_data, with_=get_num(self.puzzle_data, new_index))
			else:
				mymusicplayer.play_audio(WRONG_SOUND)
		elif event.char == "d" or event.keysym == "Right":
			new_index = blank_index - 1
			if new_index >= 0 and new_index not in resticted_number_right:
				mymusicplayer.play_audio(TILE_SOUND)
				self.puzzle_data = swife_element(self.puzzle_data, with_=get_num(self.puzzle_data, new_index))
			else:
				mymusicplayer.play_audio(WRONG_SOUND)
		elif event.char == "a" or event.keysym == "Left":
			new_index = blank_index + 1
			if new_index <= length_of_puzzle_data and new_index not in resticted_number_left:
				mymusicplayer.play_audio(TILE_SOUND)
				self.puzzle_data = swife_element(self.puzzle_data, with_=get_num(self.puzzle_data, new_index))
			else:
				mymusicplayer.play_audio(WRONG_SOUND)
		elif event.char == "q": # quit the the game
			mymusicplayer.play_audio(QUIT_SOUND)
			self.quit()

		# Checking the player Win or Not
		self.match_slidepuzzlenum_if_win()

		self.erase()
		self.slidepuzzle_look()

	def display_win_screen(self):
		global icon_dir, UNBINDING_WIDGET_NAME, GAME_LEVEL

		UNBINDING_WIDGET_NAME = "GAME"
		self.master.event_generate("<<UNBINDGUIBINDING>>")

		mymusicplayer.play_audio(WIN_SOUND)
		# Increasing Level
		self.LevelClass.increase_game_level()

		image = rand.choice(["/winpic_01.gif", "/winpic_02.gif"])

		self.main_game_frame.pack_forget() # unpacking the mainframe

		pos = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2)
		self.erase()
		
		frame = tk.Frame(self)
		frame.pack(anchor=tk.CENTER, fill=tk.BOTH)
		
		self.GifPlayer.create_animation(image_name=icon_dir+image, display_area=frame)
		
		message = "Level " + str(self.LevelClass.CURRENT_LEVEL) + " Clear"
		PopUp(self.main_parent, message)

		common_style = {"font": MENU_FONT, "bg": "Grey", "justify": tk.CENTER,
						"fg": "Green", "relief": tk.SOLID}
		
		# Main Menu button
		tk.Button(frame, text='Main Menu', image=self.game_image["back"],
			compound=tk.RIGHT,
		 command=lambda: self.display_gui_screen(widget_to_close=frame),
			 **common_style).pack(side=tk.RIGHT, fill=tk.X)
		
		# Instruction Button for player to play again
		tk.Button(frame, text="Play Again!", image=self.game_image["play_again"],
			compound=tk.RIGHT,
		  command=lambda: self.create_new_game(widget_to_close=frame),
		  **common_style).pack(side=tk.RIGHT, fill=tk.X)

		tk.Button(frame, image=self.game_image["arrow_right"], width=100,
		 command=lambda: self.move_to_next_level(widget_to_close=frame),
		 **common_style).pack(side=tk.LEFT, fill=tk.BOTH)

	def display_gui_screen(self, widget_to_close=None):
		"""This method is called when we want to return to main menu"""
		if widget_to_close:
			self.GifPlayer.close_animation()
			widget_to_close.destroy()

		mymusicplayer.play_audio(OPEN_MENU_SOUND)
		self.main_game_frame.pack_forget()
		self.gui_frame.pack(fill=tk.BOTH)
		self.bind_gui_key()

	def erase(self):
		items = self.game_canvas.find_all()
		for item in items:
			self.game_canvas.delete(item)

	def create_new_game(self, event=None, widget_to_close=None):
		"""parame: widget_to_close: if any widget needed to close before this function
			should called
		"""
		if widget_to_close:
			self.GifPlayer.close_animation()
			widget_to_close.destroy()
		
		mymusicplayer.play_audio(SHUFFLE_SOUND)
		rand.shuffle(self.puzzle_data)
		self.erase()

		# When moveing next level the new pop-up would occur
		level_message = "Level:- " + str(self.LevelClass.CURRENT_LEVEL)
		PopUp(self.main_parent, level_message)
		
		self.slidepuzzle_look()
		self.bind_key()

		# repacking the main frame ------------
		self.main_game_frame.pack(self.main_game_frame_pack_info)

	def cheat(self, event=None):
		self.puzzle_data = self.GLOBAL_PUZZLE_DATA.copy()
		mymusicplayer.play_audio(CHEAT_SOUND)
		self.erase()
		self.slidepuzzle_look()

	def match_slidepuzzlenum_if_win(self):
		# Checking the player Win or Not
		if self.GLOBAL_PUZZLE_DATA == self.puzzle_data:
			self.display_win_screen()
			return

	def move_to_next_level(self, widget_to_close=None):
		"""Method for this function to enter next level"""
	
		level = self.LevelClass.move_to_next_level()
		self.puzzle_data, self.slidepuzzle_length, self.slidepuzzle_size = load_slidepuzzlenum(level)
		self.GLOBAL_PUZZLE_DATA = self.puzzle_data.copy()

		self.create_new_game(widget_to_close=widget_to_close)
	
	def on_level_button_click(self, level, widget_to_close=None):
		"""This method called when specific button clicked in level"""
		if widget_to_close:
			widget_to_close.destroy()

		self.puzzle_data, self.slidepuzzle_length, self.slidepuzzle_size = load_slidepuzzlenum(level)
		self.GLOBAL_PUZZLE_DATA = self.puzzle_data.copy()

		level_message = "Level:- " + str(self.LevelClass.CURRENT_LEVEL) + " Set"
		PopUp(self.main_parent, level_message)

	def shuffle_button(self):
		frame = tk.Frame(self.main_game_frame, background="purple", height=30)
		frame.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.CENTER)
		
		# Button for shuffle
		# Back to the menu button
		tk.Button(frame, text="Main Menu", relief=tk.SOLID, font=TEXT_FONT,
			image=self.game_image["back"], compound=tk.RIGHT,
		 command=self.display_gui_screen).pack(side=tk.RIGHT, expand=True, fill=tk.X)
		tk.Button(frame, text='Shuffle', relief=tk.SOLID, font=TEXT_FONT,
			image=self.game_image["shuffle"], compound=tk.RIGHT,
			command=self.create_new_game).pack(side=tk.RIGHT, expand=True, fill=tk.X)
		# Button for cheat
		tk.Button(frame, text="cheat", relief=tk.SOLID, font=TEXT_FONT,
			image=self.game_image["cheat"], compound=tk.RIGHT,
		 command=self.cheat).pack(side=tk.LEFT, expand=True, fill=tk.X)

	def increase_game_volume(self, tkinter_variable: object, num=None, op: int=None):
		self.GAME_VOLUME_LEVEL.set(set_game_volume(tkinter_variable, num, op))
		message = "Volume:- " + str(self.GAME_VOLUME_LEVEL.get())
		PopUp(self.main_parent, message)
		
def load_slidepuzzlenum(length: int) -> tuple[dict, int, int]:
	"""Create the appropriate data format used in the game.

	:param length: The length of the puzzle. It should be greater than 1.
		Consider each level as '2' -> '1 level' and so on.

	:returns: A tuple containing the puzzle_data (a list of dictionaries) and
		the length (size of the puzzle display area).
	"""
	
	# list of dictionary for storing the data ({color: "name of the color", number: "number"})
	puzzle_data = []
	
	# befor looping it called a function to get the list number for the game as 'data', based on length
	for num in create_slidepuzzle_num(length):
		# "_" -> to indicate the blank space of the game.
		if num == "_":
			puzzle_data.append({"color": "red", "num": " "})
			break
		puzzle_data.append({"color": "skyblue", "num": num})
	
	return (puzzle_data, length, 240//length)

def creating_restricted_loacation_right(length):
	count = -1
	resticted_number = []
	for i in range(length):
		count += length
		resticted_number.append(count)

	return resticted_number

def creating_restricted_loacation_left(length):
	count = 0
	resticted_number = []
	for i in range(length):
		count += length
		resticted_number.append(count)

	return resticted_number

def main():
	# Calling class
	window = PreparingWindow()
	game_window = SlidePuzzle(window)
	game_window.pack(fill=tk.BOTH)

	window.mainloop()

if __name__ == '__main__':
	main()