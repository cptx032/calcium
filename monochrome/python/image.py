# coding: utf-8

import core
import utils
from PIL import Image


class ImageSprite(core.CalciumSprite):
    def __init__(self, x, y, image_path):
        self.orig_image = Image.open(image_path)
        self.image = self.orig_image.copy()
        core.CalciumSprite.__init__(
            self, x, y, dict(empty_data=[]))

    def get_pixels(self):
        image = ImageSprite.get_frame_from_image(
            self.image)
        return image

    def rotate(self, angle):
        self.image = self.orig_image.rotate(angle, expand=True)

    @staticmethod
    def get_frame_from_image_path(image_path):
        image = Image.open(image_path)
        return ImageSprite.get_frame_from_image(image)

    @staticmethod
    def get_frames_from_gif(gif_path):
        image = Image.open(gif_path)
        palette = image.getpalette()
        frames = list()
        try:
            while True:
                image.putpalette(palette)
                new_im = Image.new("RGBA", image.size)
                new_im.paste(image)
                frames.append(
                    ImageSprite.get_frame_from_image(new_im))
                image.seek(image.tell() + 1)
        except EOFError:
            pass
        return frames

    @staticmethod
    def get_frame_from_image(image):
        frame = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                gray = utils.get_gray(image, x, y)
                if gray:
                    frame.extend([x, y, gray])
        return frame

    def align(self, anchor, x, y):
        assert anchor in (
            'center', 'nw', 'n',
            'ne', 'e', 'se', 's', 'sw', 'w')
        offsetx = 0
        offsety = 0
        if anchor == 'center':
            offsetx = -int(self.image.size[0] / 2)
            offsetx = -int(self.image.size[1] / 2)
        else:
            # nice first issue
            raise NotImplementedError
        self.x = x + offsetx
        self.y = y + offsety


if __name__ == '__main__':
    import terminal
    import get_terminal_size as GTS

    class App(terminal.CalciumTerminal):
        def __init__(self, *args, **kwargs):
            terminal.CalciumTerminal.__init__(
                self, *args, **kwargs)
            self.bind('q', self.quit, '+')
            self.sprite = ImageSprite(10, 10, 'examples/lenna.png')
            self.ccounter = 0.0

        def run(self):
            # self.screen.clear()
            self.screen.plot(self.sprite)
            self.go_to_0_0()
            self.draw()
            self.ccounter += 1
            self.sprite.rotate(int(self.ccounter))

    sw, sh = GTS.get_terminal_size()
    sh *= 2
    App(sw, sh).mainloop()
