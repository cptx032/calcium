import os
import sys

from calcium import terminal
from calcium import image
from calcium import core
from calcium import draw

gif_path = os.path.join(os.path.dirname(sys.argv[0]), 'eolic.gif')


class WindFarmScene(core.CalciumScene):
    def __init__(self, window):
        super(WindFarmScene, self).__init__('mainscene', window)
        self.scene = core.CalciumSprite(
            0, 0,
            dict(normal=image.ImageSprite.get_frames_from_gif(gif_path)))
        self.line = core.CalciumSprite(0, 0, {
            'normal': [draw.line(0, 0, 80, 48, color=0)]
        })

        self.counter = 0.0
        self.sprites.append(self.scene)
        self.sprites.append(self.line)

    def run(self):
        self.counter += 1
        if self.counter >= 3:
            self.scene.next_frame()
            self.counter = 0


if __name__ == '__main__':
    app = terminal.CalciumTerminal(terminal_size=True)
    # app.set_bg_color(0xC9, 0xB9, 0x82)
    # app.set_fg_color(0x24, 0x24, 0x24)
    app.scenes['mainscene'] = WindFarmScene(app)
    app.actual_scene_name = 'mainscene'
    app.mainloop()
    print(app.last_fps)
