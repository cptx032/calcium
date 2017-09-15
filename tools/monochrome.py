# coding: utf-8
# spriter image variable_name

import sys
from PIL import Image
s = int(sys.argv[2])
image = Image.open(sys.argv[1]).resize((s, s))
pixels = []


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

for y in range(0, image.size[1], 2):
    for x in range(image.size[0]):
        top = get_gray(image, x, y)
        bottom = get_gray(image, x, y + 1)

        if top and not bottom:
            sys.stdout.write(u'▀')
        elif bottom and not top:
            sys.stdout.write(u'▄')
        elif bottom and top:
            sys.stdout.write(u'█')
        elif not bottom and not top:
            sys.stdout.write(u' ')
    sys.stdout.write(u'\n')
