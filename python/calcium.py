# coding: utf-8

import sys
import copy


def import_tkinter():
	try:
		import Tkinter as tk
	except ImportError:
		try:
			import tkinter as tk
		except ImportError:
			print('You must have Tkinter installed')
			sys.exit(-1)
	return tk


class CalciumSprite(object):
	def __init__(self, x, y, animations, frame_index=0, animation_key=None):
		self.x = x
		self.y = y
		self.animations = animations
		self.animation_key = animation_key or list(animations.keys())[0]
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

	def clone(self):
		return copy.deepcopy(self)


class CalciumScreen(object):
	LEVELS = ['█', '▓', '▒', '░']
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
