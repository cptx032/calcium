# coding utf-8

import math, typing

# RECT
def rectangle(
    width: int, height: int, color: int = 1, fill: bool = False
) -> typing.List[int]:
    u"""Return a image with a nw-anchored rectangle.

    Args:
        width, height: controls the size of rectangle
        color: 0 or 1
        fill: controls the filling of rectangle
    """
    image = list()
    for y in range(height):
        for x in range(width):
            # borders
            if (x == 0
                or y == 0
                or x == (width - 1)
                or y == (height - 1)
                or fill):
                image.extend([x, y, color])
            # fill
            elif fill:
            	for px in range(x-1, width+x):
                    for py in range(y-1, height+y):
                        image.extend([px,py,color])
    return image

# LINE
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

# OVAL
def drawOval(
    x: int, y: int, width: int, height: int, pixels, color: int
):
    sides = 1000
    for i in range(1, sides):
        pointRatio = i / sides
        radians = pointRatio * 2 * 3.14
        xSteps = math.cos(radians)
        ySteps = math.sin(radians)
        
        pointX = x + (xSteps * width)
        
        pointY = y + (ySteps * height)
        
        pixels.extend([pointX, pointY, color])

def oval(
    width: int, height: int, color: int = 1, fill: bool = False
) -> typing.List[int]:
	"""Return a pixel data with an oval.

    Args:
        width, height: controls the size of rectangle
        color: 0 or 1
        fill: controls the filling of rectangle
    """
    pixels: typing.List[int] = list()

    # borders
    if fill == False:
        drawOval(width/2, height/2, width/2, height/2, pixels, color)
    # fill
    else:
        last_px = 0
        for i in range(max(int(width/2), int(height/2))):
            drawOval((width/2), (height/2), (width/2)-i, (height/2)-i, pixels, color)
            last_px = i

        last_px = last_px + 1

        if int(width) == int(height):
            drawOval((width/2), (height/2), (width/2)-last_px, (height/2)-last_px, pixels, color)
        


    return pixels




