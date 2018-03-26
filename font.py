from datetime import datetime

from calcium.terminal import CalciumTerminal
from calcium.font import FontSprite


class ClockApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', '%H:%M:%S')
        super(ClockApp, self).__init__(*args, **kwargs)
        self.bind('q', self.quit, '+')

        # the following line works in my personal ubuntu but not in others
        # ubuntus. the idea is use a free font to use as "official" calcium
        # font
        # self.font = truetype('arial', 10)

        self.spt = FontSprite(10, 0, {'default': [[]]})

    def run(self):
        text = datetime.now().strftime(self.format)

        self.spt.text = text
        self.spt.align(
            (0.5, 0.5), self.screen.width / 2.0, self.screen.height / 2.0)
        self.screen.clear()
        self.screen.plot(self.spt)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    app = ClockApp(terminal_size=True, fps=5)
    app.mainloop()
    print(app.last_fps)
