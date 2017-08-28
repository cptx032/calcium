# coding: utf-8
import sys
sys.path.extend(['..', '.'])

def print_usage():
    print('Usage: image_viewer <image>')
    sys.exit(0)

if len(sys.argv) != 2:
    print_usage()

import window
import calcium
from PIL import Image


class ImageViewer(window.CalciumWindow):

    def run(self):
        self.clear()
        self.draw()

# preserving aspect ratio
image = Image.open(sys.argv[1])
width = 64
height = int((width * image.size[1]) / image.size[0])
image = image.resize((width, height), Image.ANTIALIAS)

pixels = []

for x in range(width):
    for y in range(height):
        a = None
        color_components = image.getpixel((x, y))
        if type(color_components) == int:
            color_components = [color_components]*3
        r, g, b = color_components[:3]
        if len(color_components) == 4:
            a = color_components[-1]

        # gray = int(0.299*r + 0.587*g + 0.114*b)
        gray = (r + g + b) / 3
        # transparency
        if a == 0:
            continue

        level = int((4*gray) / 256)
        pixels.extend([x, y, level])

sprite = calcium.CalciumSprite(
    0,
    0,
    animations={'frame_01': [pixels, ]})
top = ImageViewer(width, height)
top.add(sprite)
top.enable_escape()
top.mainloop()
