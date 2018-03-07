# coding: utf-8
import atexit
import os
import sys
import termios
import time
from calcium.get_terminal_size import get_terminal_size
import calcium.core as core

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
    ESCAPE_KEY = (27, )
    ENTER_KEY = (10, )
    ARROW_UP_KEY = (27, 91, 65)
    ARROW_DOWN_KEY = (27, 91, 66)
    ARROW_RIGHT_KEY = (27, 91, 67)
    ARROW_LEFT_KEY = (27, 91, 68)

    def __init__(self, width=None, height=None, terminal_size=False, fps=60):
        if terminal_size:
            width, height = get_terminal_size()
            height *= 2
        self.screen = core.CalciumScreen(width, height)
        self.fps = fps
        self.__run = True
        self.function_map = dict()
        init_anykey()

        # clearing the terminal
        self.clear_terminal()
        self.hide_cursor()
        self.bind(CalciumTerminal.ESCAPE_KEY, self.quit)
        atexit.register(self.__restore_terminal)

        self.last_fps = None
        self.__frame_counter = 0
        self.__fps_start_time = time.time()

    def __restore_terminal(self):
        sys.stdout.write('\033[0m')
        self.show_cursor()

    def set_fg_color(self, r, g, b):
        sys.stdout.write(
            '\033[38;2;{};{};{}m'.format(
                r, g, b))

    def set_bg_color(self, r, g, b):
        sys.stdout.write(
            '\033[48;2;{};{};{}m'.format(
                r, g, b))

    def set_fg_color_rgb(self, color):
        self.set_fg_color(*self.get_rgb_tuple_from_str(color))

    def set_bg_color_rgb(self, color):
        self.set_bg_color(*self.get_rgb_tuple_from_str(color))

    def get_rgb_tuple_from_str(self, color):
        return [int(color.replace('#', '')[i:i + 2], 16) for i in range(0, 6, 2)]

    def hide_cursor(self):
        sys.stdout.write('\033[?25l')

    def show_cursor(self):
        sys.stdout.write('\033[?25h')

    def quit(self):
        self.__run = False

    def draw(self):
        sys.stdout.write(self.screen.get_string())
        sys.stdout.flush()

    def run(self):
        u"""Function that is called every frame. Override it."""
        raise NotImplemented

    def clear_terminal(self):
        sys.stdout.write('\033[2J')

    def go_to_0_0(self):
        # go to (0, 0) position
        sys.stdout.write('\033[0;0H')

    def mainloop(self):
        while self.__run:
            start = time.time()
            key = anykey()
            if key:
                for func in self.function_map.get(tuple(key), []):
                    func()
            self.run()
            elapsed_time = time.time() - start
            sleep_time = (1.0 / self.fps) - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

            # calculating how many frames per seconds
            self.__frame_counter += 1
            if (time.time() - self.__fps_start_time) >= 1:
                self.last_fps = self.__frame_counter
                self.__frame_counter = 0
                self.__fps_start_time = time.time()

    def bind(self, key, func, op=None):
        u"""Bind a function to be called when pressing a key."""
        assert op in (None, '+', '-'), ValueError
        if type(key) != tuple:
            key = (ord(key), )
        if not self.function_map.get(key):
            self.function_map[key] = list()
        if not op:
            self.function_map[key] = list()
        list_operation = self.function_map[key].append
        if op == '-':
            list_operation = self.function_map[key].remove
        list_operation(func)
