import tkinter as tk
from PIL import Image, ImageTk


class GIF_PLAYER:
	"""
	:about: Takes a GIF file and animate it.
	"""
	def __init__(self, master):
		self.master = master
		self.image = None
		self.after_id = None

	def create_animation(self, image_name, display_area):
		"""
		:about: create a animation from a gif file
		"""
		image = Image.open(image_name)
		animation = []

		for frame in range(0, image.n_frames):
			image.seek(frame)
			animation.append(ImageTk.PhotoImage(image))

		# create a label with the first frame of the animation
		label = tk.Label(display_area, image=animation[0])
		label.pack(fill=tk.BOTH, side=tk.TOP)

		def animate(frame):
			label.config(image=animation[frame])
			self.after_id = self.master.after(50, animate, (frame + 1) % len(animation))

		self.after_id = self.master.after(0, animate, 0) # start the animation

	def close_animation(self):
		self.master.after_cancel(self.after_id) # cancel the animation