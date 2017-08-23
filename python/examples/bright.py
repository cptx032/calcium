# coding: utf-8

import sys
sys.path.extend(['..', '.'])
import calcium
import arcade
import window

class Bright(window.CalciumWindow):
	def __init__(self, size):
		window.CalciumWindow.__init__(self, size, mouse_support=True)
		self.sprite_1 = calcium.CalciumSprite(
			32, 32, animations={'run': [[0, 0, 0],]})
		self.sprite_2 = self.sprite_1.clone()
		self.sprite_2.animations['run'] = [[0,0,2],]
		self.sprite_2.x += 1
		self.add(self.sprite_1)
		self.add(self.sprite_2)

	def run(self):
		self.sprite_1.x = self.mouse_x
		self.sprite_1.y = self.mouse_y
		self.clear()
		self.draw()

top = Bright(64)
top.enable_escape()
top.mainloop()
