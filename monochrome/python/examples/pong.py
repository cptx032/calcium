# coding: utf-8
import sys
sys.path.extend(['.', '..'])
from terminal import CalciumTerminal
import core

SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32


class PongBall(core.CalciumSprite):
    def __init__(self, *args, **kwargs):
        self.velx = kwargs.pop('velx', 1)
        self.vely = kwargs.pop('vely', 1.5)
        core.CalciumSprite.__init__(self, *args, **kwargs)

    def update(self):
        self.x += self.velx
        self.y += self.vely
        if self.x >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - 1
            self.velx *= -1

        if self.y >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - 1
            self.vely *= -1

        if self.x < 0:
            self.x = 0
            self.velx *= -1

        if self.y < 0:
            self.y = 0
            self.vely *= -1


class PongApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        self.ball = PongBall(0, 0, {'normal': [[0, 0, 0]]})
        CalciumTerminal.__init__(self, *args, **kwargs)

    def run(self):
        self.ball.update()
        self.screen.fill()
        self.screen.plot(self.ball)
        self.clear_terminal()
        self.draw()

if __name__ == '__main__':
    PongApp(32, 32).mainloop()
