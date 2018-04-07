import os
import sys
from datetime import datetime

from PIL.ImageFont import truetype

from calcium.core import CalciumScene
from calcium.terminal import CalciumTerminal
from calcium.font import FontSprite


ttf_path = os.path.join(os.path.dirname(sys.argv[0]), 'Pixeled.ttf')


class ClockScene(CalciumScene):
    def __init__(self, window):
        super(ClockScene, self).__init__('clock', window)
        self.format = '%H:%M:%S'
        self.sprite = FontSprite(
            10, 0, {'default': [[]]}, font=truetype(ttf_path, 4))
        self.sprites.append(self.sprite)

    def run(self):
        self.sprite.text = datetime.now().strftime(self.format)
        self.sprite.align(
            (0.5, 0.5), self.window.screen.width / 2.0,
            self.window.screen.height / 2.0)


class ClockApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        super(ClockApp, self).__init__(*args, **kwargs)
        self.scenes['clock'] = ClockScene(self)
        self.actual_scene_name = 'clock'


if __name__ == '__main__':
    app = ClockApp(terminal_size=True, fps=5)
    app.mainloop()
