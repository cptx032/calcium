# coding: utf-8

import sys
sys.path.extend(['..', '.'])
import calcium
import arcade
import window
import baboon


class Dark(window.CalciumWindow):

    def __init__(self, size):
        window.CalciumWindow.__init__(self, size, mouse_support=True)
        self.sprite = calcium.CalciumSprite(
            0, 0, animations={'run': [baboon.baboon, ]})
        self.add(self.sprite)
        self.sprite.dark()

    def run(self):
        self.clear()
        self.draw()

top = Dark(64)
top.enable_escape()
top.mainloop()
