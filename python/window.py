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

    def __init__(self, width, height=None, fps=60):
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

    def add(self, sprite):
        """The same that world.add."""
        self.world.add(sprite)

    def clear(self):
        self.screen.clear()

    def draw(self):
        self.world.draw(self.screen)
        self.__label['text'] = str(self.screen)

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
