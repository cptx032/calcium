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
	def __init__(self, x, y, animations, frame_index=0, animation_key=None):
		self.x = x
		self.y = y
		self.animations = animations
		self.animation_key = animation_key or animations.keys()[0]
		self.frame_index = frame_index

	def get_pixels(self):
		return self.animations.get(self.animation_key)[self.frame_index]

	def next_frame(self):
		self.frame_index += 1
		if self.frame_index >= len(self.animations.get(self.animation_key)):
			self.frame_index = 0

	def last_frame(self):
		self.frame_index -= 1
		if self.frame_index < 0:
			self.frame_index = len(self.animations.get(self.animation_key)) - 1


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
		self.lines[int(y)][int(x)] = CalciumScreen.LEVELS[level]

	def plot(self, sprite):
		pixels = sprite.get_pixels()
		for i in range(0, len(pixels), 3):
			self.set_pixel(
				sprite.x + pixels[i],
				sprite.y + pixels[i + 1],
				pixels[i + 2]
			)

if __name__ == '__main__':
	import arcade
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
	13, 14, 0, 13, 15, 0, 14, 10, 0, 14, 11, 0]
	ground_pixels = [0, 0, 0, 0, 1, 0, 0, 2, 3, 0, 3, 3, 0, 4, 2, 0, 5, 2, 0, 6, 2, 0, 7, 2, 0, 8, 3, 0, 9, 2, 0, 10, 1, 0, 11, 1, 0, 12, 1, 0, 13, 1, 0, 14, 1, 0, 15, 1, 1, 0, 0, 1, 1, 0, 1, 2, 0, 1, 3, 3, 1, 4, 2, 1, 5, 2, 1, 6, 3, 1, 7, 2, 1, 8, 2, 1, 9, 2, 1, 10, 2, 1, 11, 1, 1, 12, 1, 1, 13, 2, 1, 14, 2, 1, 15, 1, 2, 0, 0, 2, 1, 0, 2, 2, 0, 2, 3, 3, 2, 4, 3, 2, 5, 2, 2, 6, 3, 2, 7, 3, 2, 8, 2, 2, 9, 2, 2, 10, 2, 2, 11, 1, 2, 12, 1, 2, 13, 2, 2, 14, 2, 2, 15, 1, 3, 0, 0, 3, 1, 0, 3, 2, 0, 3, 3, 3, 3, 4, 3, 3, 5, 2, 3, 6, 2, 3, 7, 2, 3, 8, 2, 3, 9, 2, 3, 10, 1, 3, 11, 1, 3, 12, 1, 3, 13, 1, 3, 14, 1, 3, 15, 1, 4, 0, 0, 4, 1, 0, 4, 2, 3, 4, 3, 3, 4, 4, 3, 4, 5, 3, 4, 6, 2, 4, 7, 2, 4, 8, 3, 4, 9, 2, 4, 10, 1, 4, 11, 2, 4, 12, 1, 4, 13, 1, 4, 14, 1, 4, 15, 1, 5, 0, 0, 5, 1, 0, 5, 2, 3, 5, 3, 0, 5, 4, 3, 5, 5, 3, 5, 6, 2, 5, 7, 2, 5, 8, 2, 5, 9, 2, 5, 10, 1, 5, 11, 1, 5, 12, 1, 5, 13, 1, 5, 14, 1, 5, 15, 1, 6, 0, 0, 6, 1, 0, 6, 2, 3, 6, 3, 3, 6, 4, 3, 6, 5, 2, 6, 6, 2, 6, 7, 2, 6, 8, 2, 6, 9, 1, 6, 10, 1, 6, 11, 1, 6, 12, 1, 6, 13, 1, 6, 14, 2, 6, 15, 1, 7, 0, 0, 7, 1, 0, 7, 2, 3, 7, 3, 3, 7, 4, 3, 7, 5, 2, 7, 6, 3, 7, 7, 2, 7, 8, 2, 7, 9, 1, 7, 10, 1, 7, 11, 1, 7, 12, 1, 7, 13, 1, 7, 14, 1, 7, 15, 1, 8, 0, 0, 8, 1, 0, 8, 2, 3, 8, 3, 3, 8, 4, 2, 8, 5, 2, 8, 6, 2, 8, 7, 2, 8, 8, 1, 8, 9, 1, 8, 10, 1, 8, 11, 2, 8, 12, 2, 8, 13, 1, 8, 14, 1, 8, 15, 1, 9, 0, 0, 9, 1, 0, 9, 2, 3, 9, 3, 3, 9, 4, 2, 9, 5, 2, 9, 6, 2, 9, 7, 2, 9, 8, 2, 9, 9, 1, 9, 10, 1, 9, 11, 2, 9, 12, 2, 9, 13, 2, 9, 14, 1, 9, 15, 1, 10, 0, 0, 10, 1, 0, 10, 2, 0, 10, 3, 3, 10, 4, 2, 10, 5, 2, 10, 6, 3, 10, 7, 3, 10, 8, 2, 10, 9, 2, 10, 10, 1, 10, 11, 1, 10, 12, 2, 10, 13, 2, 10, 14, 1, 10, 15, 1, 11, 0, 0, 11, 1, 0, 11, 2, 0, 11, 3, 3, 11, 4, 3, 11, 5, 2, 11, 6, 3, 11, 7, 3, 11, 8, 2, 11, 9, 2, 11, 10, 1, 11, 11, 1, 11, 12, 2, 11, 13, 2, 11, 14, 1, 11, 15, 1, 12, 0, 0, 12, 1, 0, 12, 2, 0, 12, 3, 0, 12, 4, 3, 12, 5, 2, 12, 6, 2, 12, 7, 2, 12, 8, 2, 12, 9, 2, 12, 10, 1, 12, 11, 1, 12, 12, 1, 12, 13, 1, 12, 14, 1, 12, 15, 1, 13, 0, 0, 13, 1, 0, 13, 2, 0, 13, 3, 3, 13, 4, 3, 13, 5, 2, 13, 6, 2, 13, 7, 2, 13, 8, 2, 13, 9, 2, 13, 10, 1, 13, 11, 1, 13, 12, 1, 13, 13, 1, 13, 14, 1, 13, 15, 2, 14, 0, 0, 14, 1, 0, 14, 2, 3, 14, 3, 3, 14, 4, 3, 14, 5, 2, 14, 6, 3, 14, 7, 2, 14, 8, 2, 14, 9, 1, 14, 10, 1, 14, 11, 1, 14, 12, 2, 14, 13, 1, 14, 14, 1, 14, 15, 1, 15, 0, 0, 15, 1, 0, 15, 2, 3, 15, 3, 3, 15, 4, 2, 15, 5, 2, 15, 6, 2, 15, 7, 2, 15, 8, 2, 15, 9, 1, 15, 10, 1, 15, 11, 1, 15, 12, 1, 15, 13, 1, 15, 14, 1, 15, 15, 1]
	calcium = CalciumScreen(128, 64)
	world = arcade.ArcadeWorld()

	sprite = arcade.AABBSprite(0, 0, 16, 16, animations={'running': [frame,]})
	block = arcade.AABB(0, calcium.height-16, calcium.width, 16)
	world.add(block)
	world.add(sprite)

	obstacle = arcade.AABBSprite(32,calcium.height-32, 32, 32, animations={'asd': [ground_pixels,]})
	world.add(obstacle)

	grounds = []
	for i in range(0, calcium.width, 16):
		grounds.append(CalciumSprite(i, calcium.height-16, animations={'1': [ground_pixels,]}))

	top = tk.Tk()
	top.bind('<Escape>', lambda evt: top.destroy(), '+')
	label = tk.Label(top, font=('arial', 2))
	label.pack()

	def _right(*args):
		sprite.inc_x(1)
	top.bind('<Right>', _right, '+')

	def _loop():
		sprite.inc_y(1)
		if sprite.x >= calcium.width:
			sprite.x = 0

		label['text'] = str(calcium)
		top.after(1000 / 60, _loop)

		calcium.clear()
		calcium.plot(sprite)
		calcium.plot(obstacle)

		for i in grounds:
			calcium.plot(i)
	_loop()
	top.mainloop()
