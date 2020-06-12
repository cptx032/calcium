# coding: utf-8

import random

from calcium import core, draw, filters


class RawPixelsFilter(core.BaseFilter):
    def __init__(self, pixels):
        self.pixels = pixels
        super().__init__()

    def get(self, *args):
        return self.pixels


class Particle(core.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters.append(RawPixelsFilter(draw.rectangle(2, 2)))
        self.filters.append(
            filters.PlatformPhysicsFilter(sprite=self, static=False)
        )


class MainApp(core.TerminalApplication):
    def __init__(self):
        super().__init__(terminal_size=True)
        self.sprites = list()
        self.max_particles = 20

        self.platform = core.Sprite(y=self.height - 3)
        self.platform.filters.append(
            RawPixelsFilter(draw.rectangle(self.width, 3))
        )
        self.platform.filters.append(
            filters.PlatformPhysicsFilter(sprite=self.platform, static=True)
        )
        self.sprites.append(self.platform)

        self.particle = Particle(
            x=random.randint(0, self.width - 1),
            y=random.randint(0, self.height - 10),
        )
        self.sprites.append(self.particle)

        self.bind("q", lambda *args: self.quit())
        self.bind("x", lambda *args: self.jump())

    def jump(self):
        # only jump if is touching something
        if filters.PlatformPhysicsFilter.get_over_objects(self.particle):
            filters.PlatformPhysicsFilter.apply_impulse(self.particle, 0, -1)

    def update(self):
        self.clear()
        for sprite in self.sprites:
            self.plot_sprite(sprite)
        self.draw()


if __name__ == "__main__":
    input("'x' to jump. Press ENTER")
    MainApp().run()
