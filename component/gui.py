""":about: Gui Module of the game "SlidePuzzle" """
import tkinter as tk
from tkinter import ttk

from .settings import *
# from .level_logic import Level

Images_for_menu = ["main_gui_image.png", "game.png", "about.png", "settings.png",
"back.png", "level.png"]
Images_for_about_menu = ["author.png"]
Special_images = ["link.png", "gmail.png"]

class Gui(tk.Canvas):
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		# Image variables ---------------
		self.gui_images = load_image_and_return_dict(icon_dir, Images_for_menu)
		self.about_gui_image = load_image_and_return_dict(icon_dir, Images_for_about_menu)
		self.special_images = load_image_and_return_dict(icon_dir, Special_images)

		self.create_image((WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), image=self.gui_images["main_gui_image"])

		self.parent = self.master.master
		self.gui_element()

		# Handeling Packing
		self.show()

		
	def gui_element(self):
		"""Gui element in the weiget"""
		frame = tk.Frame(self)
		frame.place(x=74, y=WINDOW_SIZE[1]//2)

		# --------Placing Widgets --------------
		option_button_width = 100
		button_bg = rbg_to_hex_converter(self.gui_images["main_gui_image"].get(x=3, y=2))
		option_button_style = {"width": option_button_width, "font": MENU_FONT,
		"relief":tk.SOLID, "compound": tk.RIGHT, "bg": button_bg}
		
		tk.Button(frame, text="Play", image= self.gui_images["game"], command=self.run_game,
		**option_button_style).grid(row=0, column=0)
		
		tk.Button(frame, text="Levels", image=self.gui_images["level"],
		command=lambda: self.display_level_screen(widget_to_close=self),
		 **option_button_style).grid(row=2, column=0)
		
		# tk.Button(frame, text="Extra", image=self.gui_images["about"],
		#  **option_button_style).grid(row=4, column=0)

		# Other Buttons
		tk.Button(self, text="About",
			image=self.gui_images["about"], justify=tk.CENTER, width=20, bg="#c1d4f5",
			command= lambda: self.display_about_screen(widget_to_close=self),
			relief=tk.SOLID).place(x=210, y=10)
		tk.Button(self, text="Setting",
			image=self.gui_images["settings"], justify=tk.CENTER, width=20, bg="#c1d4f5",
			relief=tk.SOLID, 
			command=lambda: self.display_setting_screen(widget_to_close=self)).place(x=210, y=265)
		
	def run_game(self):
		mymusicplayer.play_audio(BUTTON_SOUND_1)
		self.event_generate("<KeyPress-n>")

	def show(self, widget_to_close=None):
		"""This method is called when we want to return to main menu"""
		if widget_to_close:
			mymusicplayer.play_audio(OPEN_MENU_SOUND)
			widget_to_close.destroy()
			self.event_generate("<<ADDGUIBINDING>>")
		
		self.pack(fill=tk.BOTH)

	def display_about_screen(self, widget_to_close=None):

		if widget_to_close: # TODO WHY GLOBAL VAIRABLE IS NOT SET HERE
			self.master.master.set("GUI")
			self.event_generate("<<UNBINDGUIBINDING>>")
			widget_to_close.pack_forget()

		mymusicplayer.play_audio(BUTTON_SOUND_1)
		frame = tk.Frame(self.master)
		frame.pack(fill=tk.BOTH)
		
		notepad_bg = rbg_to_hex_converter(self.gui_images["main_gui_image"].get(x=3, y=2))
		notepad = tk.Text(frame, width=26, height=14, state=tk.DISABLED, bg=notepad_bg,
		 font=TEXT_FONT, wrap="word", padx=2, pady=2, cursor="arrow")
		self.insert_about_gui_data(notepad, extra_dir, "about.txt")
		notepad.grid(row=0, column=0, sticky=tk.NSEW)

		scroll_widget = tk.Scrollbar(frame, orient="vertical", relief=tk.FLAT,
		 command=notepad.yview)
		scroll_widget.grid(row=0, column=1, sticky=tk.NS)

		notepad.configure(yscrollcommand=scroll_widget.set)

		tk.Button(frame, text="Main Menu", font=MENU_FONT, relief=tk.GROOVE, bg=notepad_bg,
		 image=self.gui_images["back"], compound=tk.RIGHT,
		 command=lambda: self.show(widget_to_close=frame)).grid(row=1, column=0, sticky=tk.NSEW)

	def display_setting_screen(self, widget_to_close=None):

		if widget_to_close: # TODO WHY GLOBAL VAIRABLE IS NOT SET HERE
			self.master.master.set("GUI")
			self.event_generate("<<UNBINDGUIBINDING>>")
			widget_to_close.pack_forget()

		mymusicplayer.play_audio(BUTTON_SOUND_1)
		frame = tk.Frame(self.master)
		frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		tk.Label(frame, text="Game Volume", compound=tk.LEFT,
			font=MENU_FONT).pack(side=tk.TOP, fill=tk.X)
		ttk.Scale(frame, from_=1, to=100, orient="horizontal", variable=self.parent.GAME_VOLUME_LEVEL,
			command=lambda *args: set_game_volume(self.parent.GAME_VOLUME_LEVEL)).pack(side=tk.TOP, fill=tk.X)

		ttk.Separator(frame, orient="horizontal").pack(side=tk.TOP, fill=tk.X)
		tk.Button(frame, text="Main Menu", image=self.gui_images["back"],
			compound=tk.RIGHT, relief=tk.SOLID,
			command=lambda: self.show(widget_to_close=frame),
			font=MENU_FONT).pack(side=tk.BOTTOM, fill=tk.X)

	def display_level_screen(self, widget_to_close=None):

		if widget_to_close: # TODO WHY GLOBAL VAIRABLE IS NOT SET HERE
			self.master.master.set("GUI")
			self.event_generate("<<UNBINDGUIBINDING>>")
			widget_to_close.pack_forget()

		mymusicplayer.play_audio(BUTTON_SOUND_1)
		frame = tk.Frame(self.master)
		frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		level_frame = tk.Frame(frame)
		level_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		# Calling a Level class from the SlidePuzzle class
		self.parent.LevelClass.create_levels(master=level_frame, length=3)

		tk.Button(frame, text="Main Menu", image=self.gui_images["back"],
			compound=tk.RIGHT, relief=tk.SOLID,
			command=lambda: self.show(widget_to_close=frame),
			font=MENU_FONT).pack(side=tk.BOTTOM, fill=tk.X)


	def insert_about_gui_data(self, text_obj, path, filename):
		"""This method is way important for how data extract from
		text file, and how it insert it in text widget of tkinter.
		Brife Description of how it work: -> it seperate the 
		string at "$" present and than it find the word image or
		some else to do some specific functionality.
		(some other words:- image, link, email)
		"""
		fulldata = load_text_file(path, filename).split("$")

		text_obj.configure(state=tk.NORMAL)
		for data in fulldata:
			if data.split("~")[0].lower() == "image":
				image_key = data.split("~")[-1]
				text_obj.image_create("end", image=self.about_gui_image[image_key])
				continue
		
			elif data.split("~")[0].lower() == "link":
				url = data.split("~")[-1]
				common_button_style = {"text":f"[{url}]", "relief": tk.FLAT, "width": 220,
				"bg":text_obj.cget("bg"), "foreground":"blue", "activebackground": text_obj.cget("bg"),
				 "activeforeground": "yellow", "image":self.special_images["link"], "wraplength":220}
				
				button = add_hyperlink_button(text_obj, url, **common_button_style)
				text_obj.window_create("end", window=button)
				continue

			# elif data.split("~")[0].lower() == "gmail":
			# 	gmail_link = data.split("~")[-1]

			# 	common_button_style = {"text":f"[{gmail_link}]", "relief":tk.FLAT, "width": 220,
			# 	"bg": text_obj.cget("bg"), "foreground":"green", "activebackground": text_obj.cget("bg"),
			# 	"activeforeground": "yellow", "image": self.special_images["gmail"], "wraplength":220}

			# 	button = add_gmail_button(text_obj, gmail_link, **common_button_style)
			# 	text_obj.window_create("end", window=button)
			# 	continue

			text_obj.insert("end", data)

		text_obj.configure(state=tk.DISABLED)

if __name__ == '__main__':
	root = tk.Tk()
	root.wm_geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
	Gui(root, bg="purple", height=WINDOW_SIZE[1])
	root.mainloop()
