# coding: utf-8

import time

from PIL import Image

from calcium import filters
from calcium.core import BaseFilter, Sprite


def test_raw_filter():
    class RawImageFilter(BaseFilter):
        def get(self, pixels):
            return [0, 0, 1]

    sprite = Sprite()
    sprite.filters.append(RawImageFilter())
    assert sprite.get_pixels() == [0, 0, 1]


def test_invert_filter():
    class RawImageFilter(BaseFilter):
        def get(self, pixels):
            return [0, 0, 1]

    sprite = Sprite()
    sprite.filters.append(RawImageFilter())
    sprite.filters.append(filters.InvertFilter())
    assert sprite.get_pixels() == [0, 0, 0]


def test_bounds_filter():
    class RawFilter(BaseFilter):
        def get(self, pixels):
            return [-1, -2, 1, 3, 4, 1]

    sprite = Sprite()
    sprite.filters.append(RawFilter())
    sprite.filters.append(filters.BoundsFilter(sprite))
    assert sprite["minx"] == -1
    assert sprite["miny"] == -2
    assert sprite["maxx"] == 3
    assert sprite["maxy"] == 4
    assert sprite["width"] == 4
    assert sprite["height"] == 6


def test_raw_image_filter():
    image = Image.new("RGB", (1, 1))
    image.putpixel((0, 0), (255, 255, 255))

    sprite = Sprite()
    sprite.filters.append(filters.RawImageFilter(image=image))
    assert sprite.get_pixels() == [0, 0, 1]


def test_spritesheet_filter():
    # an image 1x1 black
    image01 = Image.new("RGB", (1, 1))
    image01.putpixel((0, 0), (0, 0, 0))
    # an image 1x1 white
    image02 = Image.new("RGB", (1, 1))
    image02.putpixel((0, 0), (255, 255, 255))

    sprite = Sprite()
    sprite.filters.append(
        filters.SpriteSheetFilter(images=[image01, image02], frame_delay=0.1)
    )
    # the first frame must be black
    assert sprite.get_pixels() == [0, 0, 0]
    time.sleep(0.1)
    # the first frame must be white
    assert sprite.get_pixels() == [0, 0, 1]
    # must back to black
    time.sleep(0.1)
    assert sprite.get_pixels() == [0, 0, 0]


def test_physics_colliding():
    class RawImageFilter(BaseFilter):
        def __init__(self, pixels):
            self.pixels = pixels
            super().__init__()

        def get(self, pixels):
            return self.pixels

    sprite_a = Sprite(x=0, y=0)
    sprite_a.filters.append(RawImageFilter([0, 0, 1, 10, 10, 1]))
    sprite_a.filters.append(
        filters.PlatformPhysicsFilter(sprite_a, static=True)
    )

    sprite_b = Sprite(x=11, y=11)
    sprite_b.filters.append(RawImageFilter([0, 0, 1, 10, 10, 1]))
    sprite_b.filters.append(
        filters.PlatformPhysicsFilter(sprite_b, static=True)
    )

    assert not filters.PlatformPhysicsFilter.is_colliding(sprite_a, sprite_b)
    sprite_b["x"] = 0
    sprite_b["y"] = 11
    assert not filters.PlatformPhysicsFilter.is_colliding(sprite_a, sprite_b)
    sprite_b["x"] = 0
    sprite_b["y"] = 10
    assert filters.PlatformPhysicsFilter.is_colliding(sprite_a, sprite_b)
    sprite_b["x"] = -20
    sprite_b["y"] = 5
    assert not filters.PlatformPhysicsFilter.is_colliding(sprite_a, sprite_b)
