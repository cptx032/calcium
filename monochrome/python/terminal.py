# coding: utf-8
import atexit
import os
import sys
import termios
import time
from get_terminal_size import get_terminal_size
import core

old_settings = None


def init_anykey():
    global old_settings
    old_settings = termios.tcgetattr(sys.stdin)
    new_settings = termios.tcgetattr(sys.stdin)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
    new_settings[6][termios.VMIN] = 0  # cc
    new_settings[6][termios.VTIME] = 0  # cc
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)


def anykey():
    ch_set = []
    ch = os.read(sys.stdin.fileno(), 1)
    while ch is not None and len(ch) > 0:
        # in python3 ch[0] is in anteger
        c = ch[0]
        if type(c) == int:
            c = chr(c)
        ch_set.append(ord(c))
        ch = os.read(sys.stdin.fileno(), 1)
    return ch_set

@atexit.register
def term_anykey():
    global old_settings
    if old_settings:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


class CalciumTerminal:
    Q_KEY = 113
    ESCAPE_KEY = 27

    def __init__(self, width=None, height=None, terminal_size=False, fps=60):
        if terminal_size:
            width, height = get_terminal_size()
            height *= 2
        self.screen = core.CalciumScreen(width, height)
        self.fps = fps
        self.quit_keys = [CalciumTerminal.Q_KEY, CalciumTerminal.ESCAPE_KEY]
        self.__run = True
        init_anykey()

    def quit(self):
        self.__run = False

    def draw(self):
        sys.stdout.write(self.screen.get_string())
        sys.stdout.flush()

    def run(self):
        u"""Function that is called every frame. Override it."""
        raise NotImplemented

    def clear_terminal(self):
        sys.stdout.write('\033[2J\033[1;1H')

    def mainloop(self):
        while self.__run:
            key = anykey()
            if key:
                for i in self.quit_keys:
                    if key == [i]:
                        self.__run = False
                        break
            else:
                self.run()
                time.sleep(1.0 / self.fps)
