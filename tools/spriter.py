# coding: utf-8
import sys
from PIL import Image

levels = [
	' ',
	'\xe2\x96\x91',
	'\xe2\x96\x92',
	'\xe2\x96\x93',
	'\xe2\x96\x88'
][::-1]

image = Image.open(sys.argv[1])
lines = []
for col in range(image.size[1]):
	line = []
	for li in range(image.size[0]):
		line.append('')
	lines.append(line)

for x in range(image.size[0]):
	for y in range(image.size[1]):
		r, g, b, a = image.getpixel((x, y))

		# b = pixel & 255
		# g = (pixel >> 8) & 255
		# r = (pixel >> 16) & 255

		# gray = 0.299*r + 0.587*g + 0.114*b
		gray = (r + g + b) / 3
		# print (gray, r, g, b)

		# getting levels

		if gray in range(0, 55 + 1):
			level = 0
		elif gray in range(55, 55*2 + 1):
			level = 1
		elif gray in range(55*2, 55*3 + 1):
			level = 2
		elif gray in range(55*3, 55*4 + 1):
			level = 3
		else:
			level = 4
		if a == 0:
			continue

		# lines[y][x] = levels[level] * 2

		print ', '.join([str(i) for i in [x, y, level]]) + ',',

# print '<html>'
# print '<meta charset="utf-8">'
# print '<pre style="font-size: 2pt; ">'
# print '\n'.join([''.join(i) for i in lines])
# print '</pre>'
# print '</html>'
