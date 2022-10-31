# coding: utf-8

import time
import typing

from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from calcium import core


class RawPixelsFilter(core.BaseFilter):
    def __init__(self, pixels: typing.List[int]):
        super().__init__()
        self._pixels: typing.List[int] = pixels

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        return self._pixels


class InvertFilter(core.BaseFilter):
    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        new_pixels: typing.List[int] = []

        for i in range(0, len(pixels), 3):
            x = pixels[i]
            y = pixels[i + 1]
            value = pixels[i + 2]
            new_pixels.extend([x, y, 1 - value])
        return new_pixels


class BoundsFilter(core.BaseFilter):
    """Just add a width/height property to sprite."""

    def __init__(self, sprite: core.Sprite):
        self.sprite = sprite
        self.calc_dimensions()
        super().__init__()

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        return pixels

    def calc_dimensions(self):
        data: typing.List[int] = self.sprite.get_pixels()
        minx: typing.Union[None, int] = None
        miny: typing.Union[None, int] = None
        maxx: typing.Union[None, int] = None
        maxy: typing.Union[None, int] = None
        if data:
            for i in range(0, len(data), 3):
                x = data[i]
                y = data[i + 1]
                if (minx is None) or (x < minx):
                    minx = x
                if (maxx is None) or (x > maxx):
                    maxx = x
                if (miny is None) or (y < miny):
                    miny = y
                if (maxy is None) or (y > maxy):
                    maxy = y
        else:
            minx = 0
            maxx = 0
            miny = 0
            maxy = 0

        self.sprite["minx"] = minx
        self.sprite["maxx"] = maxx

        self.sprite["miny"] = miny
        self.sprite["maxy"] = maxy

        self.sprite["width"] = maxx - minx
        self.sprite["height"] = maxy - miny


class ImageUtils:
    @staticmethod
    def get_rgb_tuple_from_str(color: str) -> typing.List[int]:
        return [
            int(color.replace("#", "")[i : i + 2], 16) for i in range(0, 6, 2)
        ]

    @staticmethod
    def get_pixels_from_image(
        image: typing.Any, threshold: float = 255 / 2
    ) -> typing.List[int]:
        data: typing.List[int] = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                value: typing.Union[int, None] = ImageUtils.get_bw_value(
                    image, x, y, threshold
                )
                if value is not None:
                    data.extend([x, y, value])
        return data

    @staticmethod
    def get_images_from_gif(gif_path) -> typing.List[typing.Any]:
        image = Image.open(gif_path)
        palette = image.getpalette()
        images = list()
        try:
            while True:
                image.putpalette(palette)
                new_im = Image.new("RGBA", image.size)
                new_im.paste(image)
                images.append(new_im)
                image.seek(image.tell() + 1)
        except EOFError:
            pass
        return images

    @staticmethod
    def get_bw_value(
        image: typing.Any, x: int, y: int, threshold: float = 255 / 2
    ) -> typing.Union[int, None]:
        a = None
        color_components = image.getpixel((x, y))
        r, g, b = None, None, None
        if type(color_components) == int:
            r, g, b = color_components, color_components, color_components
        else:
            r, g, b = color_components[:3]
            if len(color_components) == 4:
                a = color_components[-1]
                if a == 0:
                    return None

        gray = int(0.299 * r + 0.587 * g + 0.114 * b)

        if gray > threshold:
            return 1
        return 0

    @staticmethod
    def get_images_from_spritesheet(
        image_path: str, cols: int, rows: int
    ) -> typing.List[Image.Image]:
        frames: typing.List[Image.Image] = list()
        image: Image = Image.open(image_path)
        frame_width: int = int(image.size[0] / cols)
        frame_height: int = int(image.size[1] / rows)
        for y in range(0, image.size[1], frame_height):
            for x in range(0, image.size[0], frame_width):
                frame: Image.Image = image.crop(
                    (x, y, x + frame_width, y + frame_height)
                )
                frames.append(frame)
        return frames


class RawImageFilter(core.BaseFilter):
    def __init__(
        self,
        image_path: typing.Union[str, None] = None,
        image: typing.Union[typing.Any, None] = None,
        threshold: float = 255 / 2,
    ):
        if image is None and image_path is None:
            raise ValueError("You must specify the image")
        pillow_image = None
        if image:
            pillow_image = image
        else:
            pillow_image = Image.open(image_path)
        self._pixel_data: typing.List[int] = ImageUtils.get_pixels_from_image(
            pillow_image, threshold
        )
        super().__init__()

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        return self._pixel_data


class SpriteSheetFilter(core.BaseFilter):
    def __init__(
        self,
        images: typing.List[typing.Any],
        frame_delay: float = 0.1,
        threshold: float = 255 / 2,
    ):
        super().__init__()
        assert len(images) > 0
        assert frame_delay > 0

        self.frame_delay = frame_delay
        self.frames: typing.List[typing.Any] = []
        for image in images:
            if type(image) is str:
                image = Image.open(image)
            self.frames.append(
                ImageUtils.get_pixels_from_image(
                    image=image, threshold=threshold
                )
            )
        self.current_frame: int = 0
        self.timer = core.Timer()
        self.timer.after(self.frame_delay, self.next_frame)

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.timer.after(self.frame_delay, self.next_frame)

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        self.timer.tick()
        return self.frames[self.current_frame]


class PlatformPhysicsFilter(BoundsFilter):
    objects: typing.List[core.Sprite] = list()
    gravity: float = 0.1

    def __init__(
        self,
        sprite: core.Sprite,
        static: bool,
        velx: float = 0,
        vely: float = 0,
    ):
        super().__init__(sprite)
        PlatformPhysicsFilter.objects.append(sprite)
        sprite["physics_static"] = static
        sprite["velx"] = velx
        sprite["vely"] = vely
        # fixme > create a "on_touch_event"

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        if not self.sprite["physics_static"]:
            self.sprite["vely"] += PlatformPhysicsFilter.gravity
        y_increase = self.sprite["vely"]
        PlatformPhysicsFilter.y_increment(self.sprite, y_increase)
        PlatformPhysicsFilter.x_increment(self.sprite, self.sprite["velx"])
        return pixels

    @staticmethod
    def is_colliding(a: core.Sprite, b: core.Sprite) -> bool:
        """Return true when a is touching b."""
        if (a["x"] + a["maxx"]) < (b["x"] + b["minx"]):
            return False
        if (a["x"] + a["minx"]) > (b["x"] + b["maxx"]):
            return False

        if (a["y"] + a["maxy"]) < (b["y"] + b["miny"]):
            return False
        if (a["y"] + a["miny"]) > (b["y"] + b["maxy"]):
            return False
        return True

    @staticmethod
    def apply_impulse(sprite: core.Sprite, x: float, y: float) -> None:
        sprite["velx"] += x
        sprite["vely"] += y

    @staticmethod
    def get_over_objects(sprite: core.Sprite) -> typing.List[core.Sprite]:
        objects: typing.List[core.Sprite] = list()
        sprite["y"] += 1
        for obj in PlatformPhysicsFilter.objects:
            if obj == sprite:
                continue
            if PlatformPhysicsFilter.is_colliding(sprite, obj):
                objects.append(obj)
        sprite["y"] -= 1
        return objects

    @staticmethod
    def y_increment(sprite: core.Sprite, value: float) -> None:
        sprite["y"] += value
        if sprite["physics_static"]:
            return
        objs = PlatformPhysicsFilter.get_over_objects(sprite)
        if not objs:
            return
        obj = objs[0]
        if value > 0:
            sprite["y"] = obj["y"] + obj["miny"] - sprite["height"] - 1
            sprite["vely"] = 0
        elif value < 0:
            sprite["y"] = obj["y"] + obj["height"]

    @staticmethod
    def x_increment(sprite: core.Sprite, value: float) -> None:
        sprite["x"] += value
        if sprite["physics_static"]:
            return
        for obj in PlatformPhysicsFilter.objects:
            if obj == sprite:
                continue
            if PlatformPhysicsFilter.is_colliding(sprite, obj):
                if value > 0:
                    sprite["x"] = obj["x"] + obj["minx"] - sprite["width"] - 1
                    sprite["velx"] = 0
                elif value < 0:
                    sprite["x"] = obj["x"] + obj["width"]


class FlashFilter(core.BaseFilter):
    pass  # TODO


class FadeFilter(core.BaseFilter):
    def __init__(
        self,
        duration: float = 1.0,
        fadein: bool = True,
        onend: typing.Union[None, typing.Callable] = None,
    ):
        """
        Arguments:
            duration: float with the animation duration time in seconds.
            fadein: bool. If true, the animation fades in, otherwise fades out
        """
        self.duration: float = duration
        self.fadein: bool = fadein
        self.animation_x: float = 0.0
        self.last_time: typing.Union[None, float] = None
        self.onend: typing.Union[None, typing.Callable] = onend

        super().__init__()

    def restart(self):
        self.animation_x = 0.0

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        if self.last_time is None:
            self.last_time = time.time()
        time_delta = time.time() - self.last_time
        self.animation_x += time_delta / self.duration
        pixels_amount: float = len(pixels) / 3
        pixels_amount_to_show: int = int(pixels_amount * self.animation_x)
        if not self.fadein:
            pixels_amount_to_show = int(pixels_amount - pixels_amount_to_show)

        self.last_time = time.time()
        if self.animation_x >= 1.0:
            self.restart()
            if self.onend:
                self.onend()
        return pixels[: pixels_amount_to_show * 3]


class FontUtils:
    # used only to get the size of texts
    _draw: Draw = Draw(Image.new("1", (1, 1)))

    @staticmethod
    def get_font(font_path: str, font_size: int) -> typing.Any:
        return truetype(font_path, font_size)

    @staticmethod
    def get_image_from_text(
        font: typing.Any,
        text: str,
        fill: int = 1,
        align: str = "left",
        line_spacing: int = 0,
    ) -> Image:
        assert fill in (0, 1)
        assert align in ("center", "right", "left")
        image: Image = Image.new(
            "1",
            FontUtils._draw.multiline_textsize(
                text, font=font, spacing=line_spacing
            ),
        )
        drawer: Draw = Draw(image)
        drawer.multiline_text(
            (0, 0),
            text,
            font=font,
            align=align,
            fill=(255,) if fill == 1 else (0,),
            spacing=line_spacing,
        )
        return image


if __name__ == "__main__":

    class MainApp(core.TerminalApplication):
        def __init__(self):
            super().__init__()
            self.fade_filter = FadeFilter(
                duration=2, onend=self.desactive_filter
            )

            self.sprite = core.Sprite(
                filters=[
                    RawImageFilter(image_path="lenna.png"),
                    self.fade_filter,
                ]
            )
            self.bind("q", lambda *args: self.quit())

        def desactive_filter(self):
            self.fade_filter.active = False

        def update(self):
            self.clear()
            self.plot_sprite(self.sprite)
            self.draw()

    MainApp().run()
