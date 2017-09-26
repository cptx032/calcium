# coding: utf-8

import copy


class CalciumSprite(object):
    def __init__(self, x, y, animations, frame_index=0, animation_key=None):
        self.x = x
        self.y = y
        self.animations = animations
        self.animation_key = animation_key or list(animations.keys())[0]
        self.frame_index = frame_index

    def get_pixels(self):
        return self.animations.get(self.animation_key)[self.frame_index]

    def next_frame(self):
        self.frame_index += 1
        if self.frame_index >= len(self.animations.get(self.animation_key)):
            self.frame_index = 0

    def last_frame(self):
        self.frame_index -= 1
        if self.frame_index < 0:
            self.frame_index = len(self.animations.get(self.animation_key)) - 1

    def clone(self):
        return copy.deepcopy(self)

    def invert_colors(self):
        pixels = self.get_pixels()
        for i in range(0, len(pixels), 3):
            pixels[i + 2] = 3 - pixels[i + 2]

    def dark(self, level=1):
        pixels = self.get_pixels()
        for i in range(0, len(pixels), 3):
            pixels[i + 2] = max(0, pixels[i + 2] - level)

    def light(self, level=1):
        pixels = self.get_pixels()
        for i in range(0, len(pixels), 3):
            pixels[i + 2] = min(pixels[i + 2] + level, 3)


class CalciumScreen(object):
    # LEVELS = ['█', '▓', '▒', '░']
    FILLED = u'█'
    TOP = u'▀'
    BOTTOM = u'▄'
    BLANK_CHAR = u' '

    def __init__(self, width, height=None):
        u"""Represent a virtual screen."""
        self.width = width
        self.height = height or width
        assert (self.height % 2) == 0
        self.lines = []
        self.clear()

    def clear(self):
        self.__fill(0)

    def fill(self):
        self.__fill(1)

    def __fill(self, value):
        self.lines = []
        for li in range(self.height):
            line = []
            for ci in range(self.width):
                line.append(value)
            self.lines.append(line)

    def get_string(self):
        r = u''
        for y in range(0, self.height, 2):
            for x in range(self.width):
                top = self.lines[y][x]
                bottom = self.lines[y + 1][x]
                if top and bottom:
                    r += CalciumScreen.FILLED
                elif not top and not bottom:
                    r += CalciumScreen.BLANK_CHAR
                elif top and not bottom:
                    r += CalciumScreen.TOP
                elif not top and bottom:
                    r += CalciumScreen.BOTTOM
            if y <= self.height:
                r += u'\n'
        return r.encode('utf-8')[:-1]

    def __repr__(self):
        return self.get_string()

    def pixel(self, pixel, x, y):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        self.lines[y][x] = pixel

    def plot(self, sprite):
        pixels = sprite.get_pixels()
        for i in range(0, len(pixels), 3):
            self.pixel(
                sprite.x + pixels[i],
                sprite.y + pixels[i + 1],
                pixels[i + 2]
            )
