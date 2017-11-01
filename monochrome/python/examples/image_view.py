# coding: utf-8
import sys
sys.path.extend(['.', '..'])
from terminal import CalciumTerminal
import core
from PIL import Image

SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

image = Image.open(sys.argv[1])
SCREEN_WIDTH, SCREEN_HEIGHT = image.size


class ImageViewApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        self.image = core.CalciumSprite(
            0,
            0, {
                'normal': [core.CalciumSprite.get_frame_from_image(
                    sys.argv[1])]
            })
        CalciumTerminal.__init__(self, *args, **kwargs)

    def run(self):
        self.screen.fill()
        self.screen.plot(self.image)
        self.clear_terminal()
        self.draw()


if __name__ == '__main__':
    ImageViewApp(SCREEN_WIDTH, SCREEN_HEIGHT).mainloop()
