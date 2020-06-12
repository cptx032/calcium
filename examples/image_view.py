# coding: utf-8

import argparse
import sys

from PIL import Image

from calcium.core import Sprite, TerminalApplication
from calcium.filters import ImageUtils, InvertFilter, RawImageFilter


class ImageViewApp(TerminalApplication):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Shows an image in the terminal."
        )
        self.parser.add_argument("image", type=str, help="The image")
        self.parser.add_argument(
            "--bg",
            type=str,
            help="The background color in the format RRGGBB",
            metavar="RRGGBB",
            dest="bg_color",
        )
        self.parser.add_argument(
            "--fg",
            type=str,
            help="The foreground/text color in the format RRGGBB",
            metavar="RRGGBB",
            dest="fg_color",
        )
        self.parser.add_argument(
            "-i",
            help="Inverts the color of image",
            metavar="",
            dest="invert",
            const=1,
            action="store_const",
        )
        args = self.parser.parse_args()
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            sys.exit(1)

        super().__init__(terminal_size=True)
        self.sprite = Sprite()
        image = Image.open(args.image)
        image_width, image_height = image.size
        # trying adjusting width
        new_image_height = (image_height * self.width) / image_width
        if new_image_height > self.height:
            # adjusting height
            new_image_width = (image_width * self.height) / image_height
            image = image.resize((int(new_image_width), self.height))
        else:
            image = image.resize((self.width, int(new_image_height)))

        self.sprite["x"] = (self.width / 2) - (image.size[0] / 2)
        self.sprite["y"] = (self.height / 2) - (image.size[1] / 2)
        self.sprite.filters.append(RawImageFilter(image=image))
        if args.invert:
            self.sprite.filters.append(InvertFilter())

        self.bind("q", lambda *args: self.quit())
        if args.bg_color:
            self.set_bg_color(
                *ImageUtils.get_rgb_tuple_from_str(args.bg_color)
            )
        if args.fg_color:
            self.set_fg_color(
                *ImageUtils.get_rgb_tuple_from_str(args.fg_color)
            )

    def update(self):
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()


if __name__ == "__main__":
    ImageViewApp().run()
