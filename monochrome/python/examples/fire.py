# coding: utf-8
from random import randint as ri
import sys
sys.path.extend(['.', '..'])
from terminal import CalciumTerminal
import core
from get_terminal_size import get_terminal_size as GTS

SCREEN_WIDTH, SCREEN_HEIGHT = GTS()
SCREEN_HEIGHT *= 2


class Particle(core.CalciumSprite):
    DEFAULT_LIFE_TIME = 50

    def __init__(self, *args, **kwargs):
        self.velx = kwargs.pop('velx', 1)
        self.vely = kwargs.pop('vely', 1.5)
        self.lifetime = kwargs.pop(
            'lifetime', Particle.DEFAULT_LIFE_TIME)
        self.life = 0
        core.CalciumSprite.__init__(self, *args, **kwargs)
        self.initial_pos = [self.x, self.y]

    def update(self):
        self.x += self.velx
        self.y += self.vely
        self.life += 1

        if self.life >= self.lifetime:
            self.life = 0
            self.x = self.initial_pos[0]
            self.y = self.initial_pos[1]


class ParticleApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        self.particles = list()
        CalciumTerminal.__init__(self, *args, **kwargs)
        self.set_bg_color(0, 0, 0)
        self.set_fg_color(255, 100, 255)
        self.colors = []
        for i in range(20):
            self.colors.append([ri(50, 100), ri(0, 20), ri(0, 20)])
        self.screen.clear()
        self.bind(CalciumTerminal.Q_KEY, self.quit, '+')
        for i in range(500):
            self.add_particle()

    def add_particle(self):
        x = self.screen.width / 2
        x += ri(-10, 10)
        y = self.screen.height
        velx = ri(-2, 2) / 10.0
        vely = ri(-10, 0) / 10.0
        particle = Particle(
            x, y, {'normal': [[0, 0, 1]]},
            velx=velx,
            vely=vely)
        particle.life += ri(0, Particle.DEFAULT_LIFE_TIME)
        self.particles.append(particle)

    def run(self):
        self.screen.clear()
        for i in self.particles:
            i.update()
            self.screen.plot(i)
        self.go_to_0_0()
        self.draw()
        self.set_fg_color(*self.colors[ri(0, len(self.colors) - 1)])

if __name__ == '__main__':
    ParticleApp(
        SCREEN_WIDTH, SCREEN_HEIGHT).mainloop()
