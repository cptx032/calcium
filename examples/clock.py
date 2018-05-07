from datetime import datetime

from PIL.ImageFont import truetype

from calcium.core import CalciumScene
from calcium.terminal import CalciumTerminal
from calcium.font import FontSprite
from calcium.utils import local_path
from calcium.effects import InvertScreenEffect, FlashScreenEffect


ttf_path = local_path('m3x6.ttf')


class ClockScene(CalciumScene):
    def __init__(self, window):
        super(ClockScene, self).__init__('clock', window)
        self.format = '%H:%M:%S'
        self.sprite = FontSprite(
            10, 0, {'default': [[]]}, font=truetype(ttf_path, 15))
        self.sprite.effects.append(InvertScreenEffect)
        self.sprite.effects.append(FlashScreenEffect)
        self.sprites.append(self.sprite)

    def run(self):
        super(ClockScene, self).run()
        self.sprite.text = datetime.now().strftime(self.format) + ' ' + str(
            self.window.last_fps)
        self.sprite.align(
            (0.5, 0.5), self.window.screen.width / 2.0,
            self.window.screen.height / 2.0)

    def draw(self):
        self.window.screen.fill()
        super(ClockScene, self).draw()


class ClockApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        super(ClockApp, self).__init__(*args, **kwargs)
        self.scenes['clock'] = ClockScene(self)
        self.actual_scene_name = 'clock'


if __name__ == '__main__':
    app = ClockApp(terminal_size=True, fps=200)
    app.mainloop()
