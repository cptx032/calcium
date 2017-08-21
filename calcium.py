# coding: utf-8

import sys
try:
	import Tkinter as tk
except ImportError:
	try:
		import tkinter as tk
	except ImportError:
		print('You must have Tkinter installed')
		sys.exit(-1)

class CalciumSprite(object):
	def __init__(self, x, y, frames, frame_index=0):
		self.x = x
		self.y = y
		self.frames = frames
		self.frame_index = frame_index

	def get_pixels(self):
		return self.frames[self.frame_index]

	def next_frame(self):
		self.frame_index += 1
		if self.frame_index >= len(self.frames):
			self.frame_index = 0

	def last_frame(self):
		self.frame_index -= 1
		if self.frame_index < 0:
			self.frame_index = len(self.frames) - 1


class CalciumScreen(object):
	LEVELS = ['█', '▓', '▒', '░', ' ']
	def __init__(self, width, height=None, fps=60):
		self.width = width
		self.height = height or width
		self.fps = fps
		self.clear_color = 3
		self.lines = []
		self.clear()

	def clear(self):
		self.lines = []
		for li in range(self.height):
			line = []
			for ci in range(self.width):
				line.append(CalciumScreen.LEVELS[self.clear_color])
			self.lines.append(line)

	def __repr__(self):
		return '\n'.join([''.join([c + c for c in line]) for line in self.lines])

	def set_pixel(self, x, y, level):
		if x < 0 or x >= self.width:
			return
		if y < 0 or y >= self.height:
			return
		if level > 4:
			print('Calcium: invalid level value')
			return
		self.lines[y][x] = CalciumScreen.LEVELS[level]

	def plot(self, sprite):
		pixels = sprite.get_pixels()
		for i in range(0, len(pixels), 3):
			self.set_pixel(
				sprite.x + pixels[i],
				sprite.y + pixels[i + 1],
				pixels[i + 2]
			)

if __name__ == '__main__':
	frame = [0, 7, 0, 1, 8, 0, 1, 10, 0, 1, 11, 0, 2, 7, 0,
	2, 8, 0, 2, 10, 0, 2, 11, 3, 2, 12, 0, 2, 14, 0, 2, 15,
	0, 3, 7, 0, 3, 10, 0, 3, 11, 2, 3, 12, 0, 3, 13, 0, 3, 14,
	3, 3, 15, 2, 4, 6, 0, 4, 7, 0, 4, 8, 0, 4, 9, 0, 4, 10, 0,
	4, 11, 2, 4, 12, 0, 4, 13, 3, 4, 14, 1, 4, 15, 0, 5, 5, 0,
	5, 6, 3, 5, 7, 2, 5, 8, 1, 5, 9, 1, 5, 10, 1, 5, 11, 2, 5,
	12, 1, 5, 13, 2, 5, 14, 0, 6, 5, 0, 6, 6, 2, 6, 7, 2, 6, 8,
	1, 6, 9, 1, 6, 10, 1, 6, 11, 2, 6, 12, 2, 6, 13, 1, 6, 14,
	0, 7, 5, 0, 7, 6, 2, 7, 7, 2, 7, 8, 1, 7, 9, 1, 7, 10, 1, 7,
	11, 2, 7, 12, 1, 7, 13, 1, 7, 14, 0, 8, 5, 0, 8, 6, 2, 8, 7,
	2, 8, 8, 1, 8, 9, 3, 8, 10, 1, 8, 11, 2, 8, 12, 1, 8, 13, 1,
	8, 14, 0, 9, 5, 0, 9, 6, 2, 9, 7, 2, 9, 8, 1, 9, 9, 1, 9, 10,
	1, 9, 11, 2, 9, 12, 1, 9, 13, 1, 9, 14, 0, 10, 5, 0, 10, 6,
	2, 10, 7, 2, 10, 8, 1, 10, 9, 1, 10, 10, 1, 10, 11, 2, 10,
	12, 1, 10, 13, 1, 10, 14, 0, 11, 5, 0, 11, 6, 3, 11, 7, 2,
	11, 8, 1, 11, 9, 3, 11, 10, 1, 11, 11, 2, 11, 12, 2, 11, 13,
	1, 11, 14, 0, 11, 15, 0, 12, 5, 0, 12, 6, 0, 12, 7, 0, 12, 8,
	0, 12, 9, 0, 12, 10, 0, 12, 11, 0, 12, 12, 3, 12, 13, 2, 12,
	14, 2, 12, 15, 1, 13, 10, 0, 13, 11, 3, 13, 12, 0, 13, 13, 0,
	13, 14, 0, 13, 15, 0, 14, 10, 0, 14, 11, 0];
	sprite = CalciumSprite(0,0, [frame,])
	calcium = CalciumScreen(64)

	top = tk.Tk()
	label = tk.Label(top, font=('arial', 2))
	label.pack()

	def _loop():
		# sprite.x += 1
		if sprite.x >= 64:
			sprite.x = 0

		label['text'] = str(calcium)
		top.after(1000 / 60, _loop)

		calcium.clear()
		calcium.plot(sprite)
	_loop()
	top.mainloop()
