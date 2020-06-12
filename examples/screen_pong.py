# coding: utf-8

from calcium.core import TerminalApplication


class PongApp(TerminalApplication):
    def __init__(self):
        super(PongApp, self).__init__(fps=120, terminal_size=True)
        self.x = 0
        self.y = 0

        self.velx = 1
        self.vely = 1.2
        self.bind("q", lambda *args: self.quit())

    def __del__(self):
        print("Framerate: {}".format(self.last_fps))

    def update(self):
        self.go_to_0_0()
        self.set_pixel(self.x, self.y, 1)
        self.draw()

        self.x += self.velx
        self.y += self.vely

        if self.x >= self.width:
            self.velx *= -1

        if self.y >= self.height:
            self.vely *= -1

        if self.x <= 0:
            self.velx *= -1

        if self.y <= 0:
            self.vely *= -1


if __name__ == "__main__":
    PongApp().run()
