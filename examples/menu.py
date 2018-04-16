import os
import sys

from PIL.ImageFont import truetype

from calcium.core import CalciumScene, CalciumSprite
from calcium.terminal import CalciumTerminal
from calcium.draw import rectangle
from calcium.animation import Animation
from calcium.font import FontSprite


ttf_path = os.path.join(
    os.path.dirname(sys.argv[0]), 'm3x6.ttf')


class MainScene(CalciumScene):
    def __init__(self, app):
        super(MainScene, self).__init__('mainscene', app)
        self.rec = CalciumSprite(-40, 0, {
            'default': [rectangle(40, 48, fill=True)]
        })
        self.anim = Animation(
            obj=self.rec, prop='x',
            _from=-40, to=0, duration=0.5,
            loop=True, reverse_on_end=True)
        self.anim.start()
        self.fps_label = FontSprite(10, 0, {
            'default': [[]]
        }, font=truetype(ttf_path, 15), text_align='right')
        self.sprites.append(self.fps_label)
        self.sprites.append(self.rec)

    def run(self):
        self.anim.tick()
        self.fps_label.text = 'easeOutQuart\n{} fps'.format(
            self.window.last_fps)
        self.fps_label.align((1.0, 1.0), 80, 48)


app = CalciumTerminal(terminal_size=True, fps=100)
app.add_scene(MainScene(app))
app.mainloop()
