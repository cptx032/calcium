import collections

from calcium import draw
from calcium.core import CalciumSprite


class InvertScreenEffect:
    @staticmethod
    def process(screen):
        for line in screen.lines:
            for i, pixel in enumerate(line):
                line[i] = 1 - pixel


class HorizontalOffset:
    @staticmethod
    def process(screen, length=10):
        for i, line in enumerate(screen.lines):
            deque = collections.deque(line)
            deque.rotate(length)
            screen.lines[i] = list(deque)


class BorderScreenEffect:
    @staticmethod
    def process(screen):
        rec = draw.rectangle(screen.width, screen.height, fill=False)
        sprite = CalciumSprite(0, 0, {'default': [rec, ]})
        screen.plot(sprite)
