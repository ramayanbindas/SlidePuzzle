import os
import tkinter as tk
from tkinter import font
from tkinter import PhotoImage
import webbrowser

# Custom module
from .musicplayer import MyMusicPlayer

image_dir = os.path.join(os.path.abspath("."), "images") # path of image
icon_dir = os.path.join(os.path.abspath("."), "images/icon")
extra_dir = os.path.join(os.path.abspath("."), "extra")
audio_dir = os.path.join(os.path.abspath("."), "sfx")
font_dir = os.path.join(os.path.abspath("."), "font")

audio_file_list = ["open_menu.wav", "select_menu.wav", "cheat.wav", "quit.wav",
"shuffle.wav", "tile_sound.wav", "win_sound.wav", "cancel.wav"]

# Global sound constant
BUTTON_SOUND_1 = "select_menu"
OPEN_MENU_SOUND = "open_menu"
TILE_SOUND = "tile_sound"
WIN_SOUND = "win_sound"
QUIT_SOUND = "quit"
SHUFFLE_SOUND = "shuffle"
CHEAT_SOUND = "cheat"
WRONG_SOUND = "cancel"

# Global Class ---------
mymusicplayer = MyMusicPlayer()
mymusicplayer.load_audio_file(audio_dir, audio_file_list)

# Font for game
MENU_FONT = ("Comic Sans MS", 12)
LINK_FONT = "Courier New"
TEXT_FONT = ("consolas", 12)

SCREEN_SIZE = None
WINDOW_SIZE = (260, 300)
WIDGET_SEQ_AND_FUNCID = {}
WIDGET_SEQ_AND_FUNCID_NUMBER = 0

UNBINDING_WIDGET_NAME = None
UNBINDING_WIDGET_NUMBER = None

# id = [WidgetName_number]
# id: [sequence: function_id]

# def set(unbinding_widget_name: str = None, unbinding_widget_number: int = None):
# 	global UNBINDING_WIDGET_NAME, UNBINDING_WIDGET_NUMBER

# 	UNBINDING_WIDGET_NAME = unbinding_widget_name
# 	UNBINDING_WIDGET_NAME = unbinding_widget_number

# Some useful function for this game.
def create_slidepuzzle_num(length: int) -> list:
	"""This function returns the list of number for the game as to use it like a data,
		it depends on length

		:param length: length must be greate than `1` for creating appropriate game data.
	"""

	# length of slidepuzzle num is always the square to the provide lenght,
	# eg:(if length is '2' than length of slidepuzzle num in '4' on including the blank "_" space)
	# think the length as level for the game '2' -> level '1' and '3' -> level '2' and so on..
	slidepuzzle_legth = length**2
	slidepuzzle_num = []
	for num in range(1, slidepuzzle_legth+1):
		if num == slidepuzzle_legth:
			slidepuzzle_num.append("_")
			break
		slidepuzzle_num.append(str(num))

	return slidepuzzle_num

def load_image_and_return_dict(path, filelist):
	"""Function used to load all the images situated in the `path` directiories.

	:param path: Name of the path where all the images are located
	:param filelist: List of name of images along with their extension.
		eg:-["img1.png", "img2.png"]

	:return: A dictionary where the keys are the filenames (without the extension) and
		the values are the corresponding image formats usable in tkinter.
	"""
	data = {}
	for image in filelist:
		data[image.split(".")[0]] = PhotoImage(file=os.path.join(path, image))

	return data

def make_id_for_unbind(widget_name: str, sequence: str, sequence_id: str):
	""":param: id -> tkinter event id"""
	global WIDGET_SEQ_AND_FUNCID_NUMBER
	WIDGET_SEQ_AND_FUNCID_NUMBER += 1

	WIDGET_SEQ_AND_FUNCID[widget_name + "_" + str(WIDGET_SEQ_AND_FUNCID_NUMBER)] = [sequence, sequence_id]

def load_text_file(path, filename):
	"""This function used to load text file"""
	full_path = path+"/"+filename
	with open(full_path, "rt") as f:
		return f.read()

def set_game_volume(tkinter_variable: object, num=None, op: int=None):
	"""Provide op for specific increase or decrease volume
	If op provided than it must to provide num range(1, 100)
	"""
	if op == "+":
		tkinter_variable.set(tkinter_variable.get() + num)
	elif op == "-":
		tkinter_variable.set(tkinter_variable.get() - num)

	if tkinter_variable.get() >= 100:
		tkinter_variable.set(100)
	elif tkinter_variable.get() <= 0:
		tkinter_variable.set(0)

	mymusicplayer.set_volume(round(tkinter_variable.get()/100, 1))
	return tkinter_variable.get()

def rbg_to_hex_converter(rgb_value: tuple) -> str:
	"""This function convert rgb value into hexadecimal value"""
	color = "#"
	for num in rgb_value:
		if num == 0:
			color = color + "00"
			continue

		color = color + str(hex(num)[2:])

	return color

def add_hyperlink_button(master, url, **kw):
	"""This func is made for some tkinter errors:
	Error:(Tkinter can't create multiple widget with
	each different functionality)
	This function specially work for about screen gui
	for opening hyperlinks.
	"""
	
	hyperlink_font = font.Font(family=LINK_FONT, size=12, slant="italic", underline=True)

	button = tk.Button(master, cursor="hand2", font=hyperlink_font, compound=tk.LEFT,
	command=lambda: open_webbrowser(url), **kw)
	return button

# def add_gmail_button(master, gmail_link, **kw):
# 	"""This func is made for some tkinter errors:
# 	Error:(Tkinter can't create multiple widget with
# 	each different functionality)
# 	This function specially work for about screen gui
# 	for opening gmail.
# 	"""
# 	gmail_font = font.Font(family=LINK_FONT, size=12, slant="italic", underline=True)

# 	button = tk.Button(master, cursor="hand2", font=gmail_font,
# 	compound = tk.LEFT, command=lambda: open_gmail(gmail_link), **kw)
# 	return button

def open_webbrowser(url):
	try:
		webbrowser.open(url=url, new=2)
	except Exception as error:
		print(error)

# def open_gmail(gmail_link):
# 	try:
# 		webbrowser.open(url=gmail_link, new=2)
# 	except Exception as error:
# 		print(error)


if __name__ == '__main__':
	print(rbg_to_hex_converter((0, 0, 0)))