# coding utf-8

import math
import typing


def rectangle(
    width: int, height: int, color: int = 1, fill: bool = False
) -> typing.List[int]:
    u"""Return a image with a nw-anchored rectangle.

    Args:
        width, height: controls the size of rectangle
        color: 0 or 1
    """
    image = list()
    for y in range(height):
        for x in range(width):
            # borders
            if (
                x == 0
                or y == 0
                or x == (width - 1)
                or y == (height - 1)
                or fill
            ):
                image.extend([x, y, color])
    return image


def line(
    x1: float, y1: float, x2: float, y2: float, color: int = 1
) -> typing.List[int]:
    """Return a pixel data with a line."""
    pixels: typing.List[int] = list()
    dx: float = x2 - x1
    dy: float = y2 - y1
    hip: float = math.sqrt(dy ** 2 + dx ** 2)
    sin: float = dy / hip
    cos: float = dx / hip
    for i in range(int(hip)):
        x: int = math.floor((cos * i) + x1)
        y: int = math.floor((sin * i) + y1)
        pixels.extend([x, y, color])
    return pixels
