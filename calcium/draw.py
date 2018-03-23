# coding: utf-8
u"""Module to draw polygons."""


def lerp(a, b, x):
    u"""Linear interpolation."""
    return a + ((b - a) * x)


def line(x1, y1, x2, y2, color=1):
    u"""Return a image with a line with points: (x1, y1), (x2, y2)."""
    image = list()
    for x in range(x1, x2):
        c = abs(float(x) / (x2 - x1))
        y = lerp(y1, y2, c)
        image.extend([x, y, color])
    return image


def oval(width, height, color=1, border=-1):
    u"""Return a image with a nw-anchored circle/oval.

    Params:
        border: controls the width/size of border. If -1 the oval is drawn
            filled
        width, height: controls the size of oval
        color: 0 or 1
    """
    raise NotImplemented


def rectangle(width, height, color=1, border=-1):
    u"""Return a image with a nw-anchored rectangle.

    Params:
        border: controls the width/size of border. If -1 the rectangle is drawn
            filled
        width, height: controls the size of rectangle
        color: 0 or 1
    """
    raise NotImplemented


def triangle(*args):
    u"""Draw a triangle. Used to create polygons."""
    raise NotImplemented
