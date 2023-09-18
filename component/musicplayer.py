import arcade

class MyMusicPlayer():
	def __init__(self):
		self.source_list = {}
		self.current_active_player = None
		self.audio_name = None
		self.volume = 0.6
		self.pan = -1
		self.looping = False
		self.speed = 1.0
		
	def load_audio_file(self, path, list_of_audio_file):
		"""load and save audio in dictionary formate with key
		is the name of the file"""
		for audio_file in list_of_audio_file:
			self.source_list[audio_file.split(".")[0]] = arcade.load_sound(
				path+"/"+audio_file)

	def play_audio(self, name):
		"""Playe the audio file name=key"""
		try:
			if self.audio_name:
				self.current_active_player = arcade.play_sound(self.source_list[self.audio_name],
					self.volume, self.pan, self.looping, self.speed)
				return
			self.current_active_player = arcade.play_sound(self.source_list[name], self.volume, self.pan, self.looping, self.speed)
			self.audio_name = None
		except Exception as error:
			print(error)

	def stop_audio(self):
		arcade.stop_sound(self.current_active_player)

	def set_audioname(self, name):
		self.audio_name = name

	def set_volume(self, volume):
		self.volume = volume

	def set_pan(self, pan):
		self.pan = pan

	def set_looping(self, looping):
		self.looping = looping

	def set_speed(self, speed):
		self.speed = speed
		
if __name__ == '__main__':
	import tkinter as tk

	path = "C:/Users/91738/Music/Cool music"
	musics_name = ["Rabba_ya_kha_do_jara.mp3", "Life_is_strange_1.mp3"]

	myplayer = MyMusicPlayer()
	root = tk.Tk()
	myplayer.load_audio_file(path, musics_name)
	myplayer.set_audioname("Rabba_ya_kha_do_jara")
	myplayer.start()
	
	tk.Button(root, text='Press Me', command=myplayer.stop_audio).pack()
	root.mainloop()
