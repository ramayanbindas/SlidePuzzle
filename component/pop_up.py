import tkinter as tk

def PopUp(master, message: str=" ", timer: int=1):
	"""
	:param: master -> name of the master widget
	:param: message -> message should be like "level-1", "volume-3" etc
	:param: timer -> how long the message should be displayed in the screen in sec
	"""
	popup = tk.Toplevel(master)
	popup.overrideredirect(True) # Remove the title bar

	popup.wm_attributes("-topmost", True)
	
	pos_x = master.winfo_x() + 83
	pos_y = master.winfo_y() + 30

	popup.geometry(f"100x45+{pos_x}+{pos_y}") # set the geometry and the position
	popup_level_style = {"font": ("Comic Sans MS", 12), "relief":tk.SOLID, "compound":tk.CENTER}

	popup_level = tk.Label(popup, text=str(message), **popup_level_style)
	popup_level.pack(fill=tk.BOTH, expand=True)

	popup.after(timer*1000, popup.destroy)
