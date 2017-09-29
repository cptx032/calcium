# coding: utf-8


def get_gray(image, x, y):
    a = None
    color_components = image.getpixel((x, y))
    r, g, b = None, None, None
    if type(color_components) == int:
        r, g, b = color_components, color_components, color_components
    else:
        r, g, b = color_components[:3]
        if len(color_components) == 4:
            a = color_components[-1]

    gray = int(0.299 * r + 0.587 * g + 0.114 * b)

    if gray > (256 / 2.0):
        gray = 1
    else:
        gray = 0

    if a == 0:
        gray = 0

    return gray
