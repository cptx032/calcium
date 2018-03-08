# coding: utf-8

import sys
sys.path.extend(['../..', '..', '.'])
import terminal
import image
import core


class WindFarmApp(terminal.CalciumTerminal):
    def __init__(self, *args, **kwargs):
        super(WindFarmApp, self).__init__(*args, **kwargs)
        self.scene = core.CalciumSprite(
            0, 0,
            dict(normal=image.ImageSprite.get_frames_from_gif('eolic.gif')))
        self.bind('q', self.quit, '+')

        self.set_bg_color(0xC9, 0xB9, 0x82)
        self.set_fg_color(0x24, 0x24, 0x24)
        self.counter = 0.0

    def run(self):
        self.counter += 1
        if self.counter >= 3:
            self.scene.next_frame()
            self.counter = 0
        self.screen.clear()
        self.screen.plot(self.scene)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    app = WindFarmApp(terminal_size=True)
    app.mainloop()
    print(app.last_fps)
