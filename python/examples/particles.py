# coding: utf-8

import sys
sys.path.extend(['..', '.'])
import calcium
import arcade
import window
from random import randint


class Particle(arcade.ArcadePhysicsAABB):
    def __init__(self, x, y, window=None, **kwargs):
        kwargs['width'] = 1
        kwargs['height'] = 1

        self.window = window

        # self.initial_pos = [x, y]
        kwargs['vel_x'] = randint(-5, -2) / 10.0
        kwargs['vel_y'] = randint(-10, 0) / 10.0

        self.life_time = kwargs.pop('life_time', 50)
        self.life = randint(1, self.life_time)
        arcade.ArcadePhysicsAABB.__init__(self, x, y, **kwargs)

    def update(self):
        arcade.ArcadePhysicsAABB.update(self)
        self.life -= 1
        if self.life <= 0:
            self.x = self.window.mouse_x
            self.y = self.window.mouse_y
            self.life = self.life_time

            self.vel_x = randint(-15, -3) / 10.0
            self.vel_y = randint(-3, -1) / 10.0
        key = list(self.animations.keys())[0]
        color_level = int(3 - (4 * self.life) / self.life_time)
        self.animations[key][0] = [0, 0, color_level]


class ParticleWindow(window.CalciumWindow):

    MAX_SPRITES = 50

    def __init__(self, width, height=None):
        window.CalciumWindow.__init__(self, width, height, mouse_support=True)
        self.sprites = []
        for i in range(ParticleWindow.MAX_SPRITES):
            x = randint(20, 44)
            y = randint(40, 60)
            sprite = Particle(x, y, animations={'asd': [[0, 0, 0], ]}, window=self)
            self.add(sprite)

    def run(self):
        self.clear()
        self.draw()

top = ParticleWindow(128, 64)
top.title('Particles')
top.enable_escape()
top.mainloop()
