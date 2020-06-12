# coding: utf-8

"""Plot a pixel in the middle of screen."""

from calcium.core import TerminalApplication


class HelloWorldApp(TerminalApplication):
    def __init__(self):
        super(HelloWorldApp, self).__init__()
        # quit when pressing "q" key
        self.bind("q", lambda *args: self.quit())

    def update(self):
        # clears the screen
        self.clear()

        # plots the pixel in the virtual screen
        self.set_pixel(self.width / 2, self.height / 2, 1)

        # plots the virtual screen in the terminal emulator
        self.draw()


if __name__ == "__main__":
    HelloWorldApp().run()
