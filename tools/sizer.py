# coding: utf-8
# sizer origin_image new_width new_height dest_path
import sys
from PIL import Image

width, height = int(sys.argv[2]), int(sys.argv[3])

image = Image.open(sys.argv[1])
image.resize((width, height)).save(sys.argv[4])
