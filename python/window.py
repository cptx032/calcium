# coding: utf-8
"""Tkinter implementation of Calcium."""
import arcade
import calcium
import sys


def import_tkinter():
    """Import the correct version of Tkinter."""
    try:
        import Tkinter as tk
    except ImportError:
        try:
            import tkinter as tk
        except ImportError:
            print('You must have Tkinter installed')
            sys.exit(-1)
    return tk

tk = import_tkinter()


class CalciumWindow(tk.Tk):
    """Represent a complete Calcium Screen made in Tkinter."""

    def __init__(self, width, height=None, fps=60, mouse_support=False):
        u"""
        Create a Tkinter window instance.

            width: how many pixels in horizontal the screen must have
        """
        self.screen = calcium.CalciumScreen(width, height)
        self.world = arcade.ArcadeWorld()
        self.fps = fps
        tk.Tk.__init__(self)
        self.configure(border=0)
        self.__label = tk.Label(
            self, font=('arial', 2),
            border=0, highlightthickness=0)
        self.__label.grid()

        self.mouse_x = 0
        self.mouse_y = 0

        if mouse_support:
            self.enable_mouse_position()

    def get_font(self):
        return self.__label['font']

    def set_font(self, font):
        self.__label['font'] = font

    def enable_mouse_position(self):
        self.bind('<Motion>', self.__store_mouse_coords, '+')
        self.bind('<Button-1>', self.__store_mouse_coords, '+')

    def __store_mouse_coords(self, evt):
        self.mouse_x = (self.screen.width * evt.x) / self.get_real_width()
        self.mouse_y = (self.screen.height * evt.y) / self.get_real_height()

    def add(self, sprite):
        """The same that world.add."""
        self.world.add(sprite)

    def get_real_width(self):
        return self.__label.winfo_width()

    def get_real_height(self):
        return self.__label.winfo_height()

    def clear(self):
        self.screen.clear()

    def draw(self):
        self.world.draw(self.screen)
        self.__label['text'] = self.screen.get_string()

    def run(self, func):
        u"""Run method is called every frame.

        You must override this function"""
        raise NotImplementedError()

    def __execute_run(self):
        self.run()
        self.after(int(1000 / self.fps), self.__execute_run)

    def enable_escape(self):
        self.bind('<Escape>', lambda evt: self.destroy(), '+')

    def mainloop(self):
        self.__execute_run()
        tk.Tk.mainloop(self)
