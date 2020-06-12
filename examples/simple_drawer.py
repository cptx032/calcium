# coding: utf-8

"""Plot a pixel in the middle of screen."""

from calcium.core import TerminalApplication


class SimpleDrawerApp(TerminalApplication):
    def __init__(self):
        super(SimpleDrawerApp, self).__init__(terminal_size=True, fps=1000)
        # quit when pressing "q" key
        self.cursor_x = self.width / 2
        self.cursor_y = self.height / 2
        self.points = []
        self.bind("q", lambda *args: self.quit())
        self.bind("x", lambda *args: self.save_pixel())
        self.bind(self.ARROW_UP_KEY, lambda *args: self.move_up())
        self.bind(self.ARROW_DOWN_KEY, lambda *args: self.move_down())
        self.bind(self.ARROW_LEFT_KEY, lambda *args: self.move_left())
        self.bind(self.ARROW_RIGHT_KEY, lambda *args: self.move_right())

    def move_left(self):
        self.cursor_x -= 1
        if self.cursor_x < 0:
            self.cursor_x = self.width - 1

    def move_right(self):
        self.cursor_x += 1
        if self.cursor_x >= self.width:
            self.cursor_x = 0

    def move_up(self):
        self.cursor_y -= 1
        if self.cursor_y < 0:
            self.cursor_y = self.height - 1

    def move_down(self):
        self.cursor_y += 1
        if self.cursor_y >= self.height:
            self.cursor_y = 0

    def save_pixel(self):
        self.points.append([self.cursor_x, self.cursor_y, 1])

    def update(self):
        # clears the screen
        self.clear()

        # plots the cursor in the virtual screen
        self.set_pixel(self.cursor_x, self.cursor_y, 1)

        # ploting all saved points
        for point in self.points:
            self.set_pixel(*point)

        # plots the virtual screen in the terminal emulator
        self.draw()


if __name__ == "__main__":
    input(
        "Move the cursor with the arrow keys. Press 'x' for paint. Press ENTER"
    )
    SimpleDrawerApp().run()
