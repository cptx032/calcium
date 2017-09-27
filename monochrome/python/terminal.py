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


@atexit.register
def term_anykey():
    global old_settings
    if old_settings:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


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

    def quit(self):
        self.__run = False

    def run(self):
        u"""Function that is called every frame. Override it."""
        raise NotImplemented

    def mainloop(self):
        while self.__run:
            key = self.any_key()
            if key:
                for i in self.quit_keys:
                    if key == [i]:
                        self.__run = False
                        break
            else:
                self.run()

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

FPS = 60
if __name__ == '__main__':
    Q_KEY = 113
    ESCAPE_KEY = 27

    size = list(get_terminal_size())
    # duplicating the size in 'y' axis because in 'monochrome' mode
    # each character represents 2 characters. to fill all the screen
    size[1] *= 2
    screen = core.CalciumScreen(*size)
    init_anykey()

    o = core.CalciumSprite(0, 0, {'normal': [[0, 0, 0]]})

    while True:
        key = anykey()
        if key:
            if key == [Q_KEY] or key == [ESCAPE_KEY]:
                break
        else:
            o.x += 1
            if o.x >= screen.width:
                o.x = 0
                o.y += 1
                if o.y >= screen.height:
                    o.y = 0
            screen.fill()
            # screen.pixel(1, o.x, o.y)
            screen.plot(o)
            # clear screen
            sys.stdout.write('\033[2J\033[1;1H')
            sys.stdout.write(screen.get_string())
            time.sleep(FPS / 1000.0)
