# coding: utf-8
import atexit
import os
import sys
import termios
import time
from calcium.get_terminal_size import get_terminal_size_in_pixels
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


class CalciumTerminal(core.GenericWindow):
    ESCAPE_KEY = (27, )
    ENTER_KEY = (10, )
    ARROW_UP_KEY = (27, 91, 65)
    ARROW_DOWN_KEY = (27, 91, 66)
    ARROW_RIGHT_KEY = (27, 91, 67)
    ARROW_LEFT_KEY = (27, 91, 68)

    def __init__(self, width=None,
                 height=None, terminal_size=False, fps=60,
                 center=False):
        available_width, available_height = get_terminal_size_in_pixels()
        if terminal_size:
            width, height = available_width, available_height
        else:
            if width > available_width or (height and height > available_height):
                raise ValueError(
                    'The width/height must be less than or equal the available'
                    ' width/height ({}, {})'.format(
                        available_width, available_height))
        if not height:
            height = width
        offsetx = 0
        offsety = 0
        if center:
            offsetx = int((available_width / 2.0) - (width / 2.0))
            offsety = int((available_height / 2.0) - (height / 2.0))
        super(CalciumTerminal, self).__init__(
            width=width, height=height, offsetx=offsetx, offsety=offsety,
            fps=fps)
        init_anykey()

        # clearing the terminal
        self.go_to_0_0()
        self.blank_terminal()
        self.go_to_0_0()
        self.hide_cursor()
        atexit.register(self.__restore_terminal)

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

    def draw(self):
        sys.stdout.write(self.screen.get_string())
        sys.stdout.flush()

    def clear(self):
        self.go_to_0_0()

    def go_to_0_0(self):
        # go to (0, 0) position
        sys.stdout.write('\033[0;0H')

    def blank_terminal(self):
        sys.stdout.write('\033[2J')

    def process_input(self):
        key = anykey()
        if key:
            for func in self.scene.function_map.get(tuple(key), []):
                func()

    def mainloop(self):
        while self.keep_running:
            self.next_frame()
