# coding: utf-8
import sys
sys.path.extend(['.', '..'])
from terminal import CalciumTerminal
import core
from PIL import Image

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
        self.bind('q', self.quit, '+')

    def run(self):
        self.screen.clear()
        self.screen.plot(self.image)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    ImageViewApp(SCREEN_WIDTH, SCREEN_HEIGHT).mainloop()
