"""effects.py is a experimental module for making effects in virtual screen."""
import collections

from calcium import draw
from calcium.core import CalciumSprite
from calcium.core import Timer


class InvertScreenEffect:
    @staticmethod
    def process(screen):
        # benchmark who is more faster
        # screen.lines = [[int(not col) for col in line] for line in screen.lines]
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


class FlashScreenEffect:
    """Flash/flick the screen in a specific frequency."""

    timer = Timer()
    active = True
    screen = None
    _binded = False
    frequency = 2
    # states: 0 - normal 1 - inverted
    state = 0

    @staticmethod
    def _process():
        if FlashScreenEffect.active:
            # toggle boolean
            FlashScreenEffect.state = int(not FlashScreenEffect.state)

            FlashScreenEffect.timer.after(
                FlashScreenEffect.frequency, FlashScreenEffect._process)

    @staticmethod
    def process(screen, frequency=0.1):
        """Will be called every frame."""
        FlashScreenEffect.screen = screen
        FlashScreenEffect.frequency = frequency

        if not FlashScreenEffect._binded:
            FlashScreenEffect.timer.after(
                frequency, FlashScreenEffect._process)
            FlashScreenEffect._binded = True

        if FlashScreenEffect.state == 1:
            InvertScreenEffect.process(FlashScreenEffect.screen)

        FlashScreenEffect.timer.tick()
