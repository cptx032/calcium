# coding: utf-8

import os

from calcium.core import Sprite, TerminalApplication
from calcium.filters import ImageUtils, SpriteSheetFilter

BASE_FOLDER = os.path.dirname(os.path.realpath(__file__))


class MyApp(TerminalApplication):
    def __init__(self):
        super(MyApp, self).__init__()
        self.sprite = Sprite()
        self.sprite.filters.append(
            SpriteSheetFilter(
                frame_delay=0.045,
                images=ImageUtils.get_images_from_gif(
                    os.path.join(BASE_FOLDER, "flag.gif")
                ),
            )
        )
        self.bind("q", lambda *args: self.quit(), "+")
        self.set_fg_color(0x0E, 0x3C, 0x5D)
        self.set_bg_color(0, 0, 0)

    def update(self):
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()


if __name__ == "__main__":
    MyApp().run()
