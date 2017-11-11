# coding: utf-8

import sys
sys.path.extend(['../..', '..', '.'])
from get_terminal_size import get_terminal_size as GTS
import terminal
import image
import core


class SpriteSheetApp(terminal.CalciumTerminal):
    def __init__(self, *args, **kwargs):
        terminal.CalciumTerminal.__init__(self, *args, **kwargs)
        self.character = core.CalciumSprite(
            10, self.screen.height-16,
            dict(
                normal=image.ImageSprite.get_frames_from_sheet(
                    'sheet.png', 6, 1)))
        self.bind('q', self.quit, '+')

        self.set_bg_color(0xC9, 0xB9, 0x82)
        self.set_fg_color(0x24, 0x24, 0x24)
        self.counter = 0.0

    def run(self):
        self.counter += 1
        if self.counter >= 5:
            self.character.next_frame()
            self.counter = 0
        self.screen.clear()
        self.screen.plot(self.character)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    w, h = GTS()
    h *= 2
    SpriteSheetApp(w, h).mainloop()
