from datetime import datetime

from calcium.terminal import CalciumTerminal
from calcium.font import FontSprite


class ClockApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', '%H:%M:%S')
        super(ClockApp, self).__init__(*args, **kwargs)
        self.bind('q', self.quit, '+')

        self.sprite = FontSprite(10, 0, {'default': [[]]})

    def run(self):
        text = datetime.now().strftime(self.format)

        self.sprite.text = text
        self.sprite.align(
            (0.5, 0.5), self.screen.width / 2.0, self.screen.height / 2.0)
        self.screen.clear()
        self.screen.plot(self.sprite)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    app = ClockApp(terminal_size=True, fps=5)
    app.mainloop()
    print(app.last_fps, 'fps')
