"""Module to draw polygons."""


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


def rectangle(width, height, color=1, fill=False):
    u"""Return a image with a nw-anchored rectangle.

    Args:
        width, height: controls the size of rectangle
        color: 0 or 1
    """
    image = list()
    for y in range(height):
        for x in range(width):
            # borders
            if x == 0 or y == 0 or x == (width - 1) or y == (height - 1) or fill:
                image.extend([x, y, color])
    return image
