# coding: utf-8

import sys
sys.path.extend(['../..', '..', '.'])
from get_terminal_size import get_terminal_size as GTS
import terminal
import image
import core
import arcade


def rectangle(width, height, value=1):
    charactels = list()  # character pixels
    for y in range(height):
        for x in range(width):
            charactels.extend([x, y, value])
    return charactels


class PlatformApp(terminal.CalciumTerminal):
    def __init__(self, *args, **kwargs):
        terminal.CalciumTerminal.__init__(self, *args, **kwargs)
        x, y = 10, self.screen.height - 30
        wi, he = self.screen.width - 20, 5
        self.world = arcade.ArcadeWorld()
        self.rectangle = arcade.ArcadePhysicsAABB(
            10, 10, 3, 3,
            {'normal': [rectangle(3, 3)]})
        self.rectangle.vel_y = 1
        self.world.add(arcade.ArcadePhysicsAABB(
            x, y, wi, he,
            {'normal': [rectangle(wi, he)]}))
        self.world.add(arcade.ArcadePhysicsAABB(
            0, 38, 180, 10,
            {'normal': [rectangle(180, 10)]}))
        self.world.add(self.rectangle)

        self.__binds()
        self.set_fg_color(0xC9, 0xB9, 0x82)
        self.set_bg_color(0x24, 0x24, 0x24)

    def __binds(self):
        self.bind(
            terminal.CalciumTerminal.ARROW_UP_KEY, self.__up, '+')
        self.bind(
            terminal.CalciumTerminal.ARROW_DOWN_KEY, self.__down, '+')
        self.bind(
            terminal.CalciumTerminal.ARROW_LEFT_KEY, self.__left, '+')
        self.bind(
            terminal.CalciumTerminal.ARROW_RIGHT_KEY, self.__right, '+')
        self.bind('q', self.quit, '+')

    def __up(self):
        # checking bounds
        if self.rectangle.y > 0:
            self.rectangle.inc_y(-2)  # greater than gravity

    def __down(self):
        if (self.rectangle.y + self.rectangle.height) < self.screen.height:
            self.rectangle.inc_y(1)

    def __left(self):
        if self.rectangle.x > 0:
            self.rectangle.inc_x(-1)

    def __right(self):
        if (self.rectangle.x + self.rectangle.width) < self.screen.width:
            self.rectangle.inc_x(1)

    def run(self):
        self.screen.clear()
        self.world.draw(self.screen)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    w, h = GTS()
    h *= 2
    PlatformApp(w, h).mainloop()
