from calcium.terminal import CalciumTerminal
from calcium import core
from calcium.get_terminal_size import get_terminal_size as GTS

SCREEN_WIDTH, SCREEN_HEIGHT = GTS()
SCREEN_HEIGHT *= 2


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


class PongScene(core.CalciumScene):
    def __init__(self, window):
        super(PongScene, self).__init__('mainscene', window)
        self.ball = PongBall(0, 0, {'normal': [[0, 0, 1]]}, velx=3, vely=2)
        self.bind(
            CalciumTerminal.ARROW_RIGHT_KEY,
            self.__change_bg_color,
            '+'
        )
        self.sprites.append(self.ball)

    def __change_bg_color(self):
        self.window.set_bg_color(255, 0, 0)

    def run(self):
        self.ball.update()

if __name__ == '__main__':
    app = CalciumTerminal(fps=60, terminal_size=True)
    app.set_fg_color(0xec, 0xf0, 0xf1)
    app.set_bg_color(0x2e, 0xcc, 0x71)
    app.scenes['mainscene'] = PongScene(app)
    app.actual_scene_name = 'mainscene'
    app.mainloop()
