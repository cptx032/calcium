import os
import sys

from calcium.terminal import CalciumTerminal
from calcium import core
from PIL import Image


def print_usage():
    print('Usage:\n\t{} image_path.ext'.format(sys.argv[0]))

if len(sys.argv) == 1:
    print_usage()
    sys.exit(-1)

if not os.path.exists(sys.argv[1]):
    print_usage()
    sys.exit(-1)


if '--help' in sys.argv:
    print_usage()
    sys.exit(0)

image = Image.open(sys.argv[1])
SCREEN_WIDTH, SCREEN_HEIGHT = image.size

fg = None
bg = None

if '-fg' in sys.argv:
    fg = sys.argv[sys.argv.index('-fg') + 1]

if '-bg' in sys.argv:
    bg = sys.argv[sys.argv.index('-bg') + 1]


class ImageScene(core.CalciumScene):
    def __init__(self, window):
        super(ImageScene, self).__init__('image', window)
        self.sprites.append(
            core.CalciumSprite(
                0,
                0, {
                    'normal': [core.CalciumSprite.get_frame_from_image(
                        sys.argv[1])]
                })
        )
        self.bind('q', self.window.quit, '+')

    def run(self):
        pass


class ImageViewApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        CalciumTerminal.__init__(self, *args, **kwargs)
        self.add_scene(ImageScene(self))
        if fg:
            self.set_fg_color_rgb(fg)
        if bg:
            self.set_bg_color_rgb(bg)


if __name__ == '__main__':
    ImageViewApp(SCREEN_WIDTH, SCREEN_HEIGHT).mainloop()
