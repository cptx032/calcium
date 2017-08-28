# coding: utf-8
# spriter image variable_name

import sys
from PIL import Image

image = Image.open(sys.argv[1])
pixels = []

for x in range(image.size[0]):
    for y in range(image.size[1]):
        a = None
        color_components = image.getpixel((x, y))
        r, g, b = color_components[:3]
        if len(color_components) == 4:
            a = color_components[-1]

        # gray = int(0.299*r + 0.587*g + 0.114*b)
        gray = (r + g + b) / 3

        if a == 0:
            continue

        level = int((4 * gray) / 256)

        # lines[y][x] = level
        pixels.extend([x, y, level])

print sys.argv[2], '=', pixels
# print '<html>'
# print '<meta charset="utf-8">'
# print '<pre style="font-size: 2pt; ">'
# print '\n'.join([''.join(i) for i in lines])
# print '</pre>'
# print '</html>'
