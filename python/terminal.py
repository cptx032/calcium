# coding: utf-8
import atexit
import os
import sys
import termios
import time
import terminal_calcium

old_settings=None

def init_anykey():
    global old_settings
    old_settings = termios.tcgetattr(sys.stdin)
    new_settings = termios.tcgetattr(sys.stdin)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
    new_settings[6][termios.VMIN] = 0  # cc
    new_settings[6][termios.VTIME] = 0 # cc
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

@atexit.register
def term_anykey():
    global old_settings
    if old_settings:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def anykey():
    ch_set = []
    ch = os.read(sys.stdin.fileno(), 1)
    while ch != None and len(ch) > 0:
        ch_set.append( ord(ch[0]) )
        ch = os.read(sys.stdin.fileno(), 1)
    return ch_set


class O:
    def __init__(self):
        self.x = 0
        self.y = 0

FPS = 60
if __name__ == '__main__':
    Q_KEY = 113
    ESCAPE_KEY = 27
    screen = terminal_calcium.CalciumScreen(80, 48)
    init_anykey()

    o = O()
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
            screen.clear()
            screen.pixel(1, o.x, o.y)
            sys.stdout.write('\033[2J\033[1;1H')
            sys.stdout.write(screen.get_string())
            time.sleep(FPS / 1000.0)
