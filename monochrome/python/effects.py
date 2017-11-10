# coding: utf-8
import collections


class InvertEffect:
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
