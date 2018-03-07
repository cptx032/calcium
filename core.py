# coding: utf-8

import copy
import calcium.utils as utils


class CalciumSprite(object):
    def __init__(
            self, x, y,
            animations, frame_index=0,
            animation_key=None,
            size=None, visible=True):
        self.x = x
        self.y = y
        self.visible = visible
        self.animations = animations
        self.animation_key = animation_key or list(animations.keys())[0]
        self.frame_index = frame_index
        self.size = size
        if not size:
            self.size = CalciumSprite.get_size_from_pixels(
                self.get_pixels())

    def is_touching(self, sprite):
        if self.x > (sprite.x + sprite.size[0]):
            return False
        if sprite.x > (self.x + self.size[0]):
            return False
        if self.y > (sprite.y + sprite.size[1]):
            return False
        if sprite.y > (self.y + self.size[1]):
            return False
        return True

    @staticmethod
    def get_size_from_pixels(pixels):
        width = 0
        height = 0
        for i in range(0, len(pixels), 3):
            x = pixels[i]
            y = pixels[i + 1]
            if x > width:
                width = x
            if y > height:
                height = y
        # cause coordenates starts in (0, 0) we must
        # sum 1
        return (width + 1, height + 1)

    def align(self, anchor, x, y):
        offsetx = -self.size[0] * anchor[0]
        offsety = -self.size[1] * anchor[1]
        self.x = x + offsetx
        self.y = y + offsety

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

    @staticmethod
    def get_frame_from_image(image_path):
        from PIL import Image
        image = Image.open(image_path)
        frame = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                frame.extend([x, y, utils.get_gray(image, x, y)])
        return frame

    def add_frame_from_image(self, image_path):
        self.animations[self.animation_key].append(
            self.get_frame_from_image(image_path))


class CalciumScreen(object):
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
        return r[:-1]

    def __repr__(self):
        return self.get_string()

    def pixel(self, x, y, pixel):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        self.lines[int(y)][int(x)] = pixel

    def plot(self, sprite):
        if not sprite.visible:
            return
        pixels = sprite.get_pixels()
        for i in range(0, len(pixels), 3):
            self.pixel(
                sprite.x + pixels[i],
                sprite.y + pixels[i + 1],
                pixels[i + 2]
            )