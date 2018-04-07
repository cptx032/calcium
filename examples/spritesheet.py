import os
import sys

from calcium.get_terminal_size import get_terminal_size as GTS
from calcium import terminal
from calcium import image
from calcium import core


class MainScene(core.CalciumScene):
    def __init__(self, window):
        super(MainScene, self).__init__('main', window)
        self.character = core.CalciumSprite(
            10, self.window.screen.height - 16,
            dict(
                normal=image.ImageSprite.get_frames_from_sheet(
                    os.path.join(os.path.dirname(sys.argv[0]), 'sheet.png'), 6, 1)))
        self.sprites.append(self.character)
        self.bind('q', self.window.quit, '+')
        self.counter = 0.0

    def run(self):
        self.counter += 1
        if self.counter >= 5:
            self.character.next_frame()
            self.counter = 0


class SpriteSheetApp(terminal.CalciumTerminal):
    def __init__(self, *args, **kwargs):
        terminal.CalciumTerminal.__init__(self, *args, **kwargs)
        self.add_scene(MainScene(self))

        self.set_bg_color(0xC9, 0xB9, 0x82)
        self.set_fg_color(0x24, 0x24, 0x24)


if __name__ == '__main__':
    w, h = GTS()
    h *= 2
    SpriteSheetApp(w, h).mainloop()
