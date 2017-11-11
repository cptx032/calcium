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


class ParticleGenerator:
    def __init__(self, x, y, width, height, **kws):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.particles = list()
        self.default_life_time = kws.pop(
            'default_life_time', 50)
        self.velx_range = kws.pop('velx_range', [-2, 2])
        self.vely_range = kws.pop('vely_range', [-10, 0])
        self.particle_data = kws.pop(
            'particle_data', [[0, 0, 1]])

    def create_particles(self, num_particles, random_life=True):
        for i in range(num_particles):
            x = ri(int(self.x), int(self.x + self.width))
            y = ri(int(self.y), int(self.y + self.height))
            velx = ri(*self.velx_range) / 10.0
            vely = ri(*self.vely_range) / 10.0
            particle = Particle(
                x, y, {'normal': self.particle_data},
                velx=velx,
                vely=vely)
            if random_life:
                particle.life += ri(0, self.default_life_time)
            self.particles.append(particle)

    def clear(self):
        self.particles = list()

    def draw(self, screen):
        for particle in self.particles:
            particle.update()
            screen.plot(particle)


if __name__ == '__main__':
    class ParticleApp(CalciumTerminal):
        def __init__(self, *args, **kwargs):
            CalciumTerminal.__init__(self, *args, **kwargs)
            self.set_bg_color(0, 0, 0)
            self.set_fg_color(255, 100, 255)
            self.colors = []
            for i in range(20):
                self.colors.append([ri(50, 100), ri(0, 20), ri(0, 20)])
            self.screen.clear()
            self.bind(CalciumTerminal.Q_KEY, self.quit, '+')
            width = 20
            self.particle_gen = ParticleGenerator(
                (self.screen.width / 2) - (width / 2),
                self.screen.height-5,
                width,
                5)
            self.particle_gen.create_particles(500)

        def run(self):
            self.screen.clear()
            self.particle_gen.draw(self.screen)
            self.go_to_0_0()
            self.draw()
            self.set_fg_color(*self.colors[ri(0, len(self.colors) - 1)])
    ParticleApp(
        SCREEN_WIDTH, SCREEN_HEIGHT).mainloop()
