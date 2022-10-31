from calcium import core, draw, filters


class RawPixelsFilter(core.BaseFilter):
    def __init__(self, pixels):
        self.pixels = pixels
        super().__init__()

    def get(self, *args):
        return self.pixels


class DrawOval(core.TerminalApplication):
    def __init__(self):
        super(DrawOval, self).__init__(terminal_size=True, fps=1000)
        # quit when pressing "q" key
        self.bind("q", lambda *args: self.quit())
        self.set_fg_color(225, 0, 255)
        self.points = []

    def update(self):
        # clears the screen
        self.clear()

        self.sprites = list()

        # test1
        self.platform = core.Sprite(x=5, y=0)
        self.platform.filters.append(RawPixelsFilter(draw.rectangle(15, 10, 1, True)))
        self.sprites.append(self.platform)
        
        self.oval = core.Sprite(x=5, y=11)
        self.oval.filters.append(RawPixelsFilter(draw.oval(15, 10, 1, False)))
        self.sprites.append(self.oval)

        self.oval = core.Sprite(x=21, y=0)
        self.oval.filters.append(RawPixelsFilter(draw.oval(15, 10, 1, True)))
        self.sprites.append(self.oval)


        # test2
        self.platform = core.Sprite(x=5, y=45)
        self.platform.filters.append(RawPixelsFilter(draw.rectangle(10, 16, 1, True)))
        self.sprites.append(self.platform)
        
        self.oval = core.Sprite(x=5, y=66)
        self.oval.filters.append(RawPixelsFilter(draw.oval(10, 16, 1, False)))
        self.sprites.append(self.oval)

        self.oval = core.Sprite(x=21, y=45)
        self.oval.filters.append(RawPixelsFilter(draw.oval(10, 16, 1, True)))
        self.sprites.append(self.oval)

        # test3
        self.platform = core.Sprite(x=50, y=0)
        self.platform.filters.append(RawPixelsFilter(draw.rectangle(23, 10, 1, True)))
        self.sprites.append(self.platform)
        
        self.oval = core.Sprite(x=50, y=11)
        self.oval.filters.append(RawPixelsFilter(draw.oval(23, 10, 1, False)))
        self.sprites.append(self.oval)

        self.oval = core.Sprite(x=74, y=0)
        self.oval.filters.append(RawPixelsFilter(draw.oval(23, 10, 1, True)))
        self.sprites.append(self.oval)

        # test4
        self.platform = core.Sprite(x=50, y=45)
        self.platform.filters.append(RawPixelsFilter(draw.rectangle(13, 13, 1, True)))
        self.sprites.append(self.platform)
        
        self.oval = core.Sprite(x=64, y=45)
        self.oval.filters.append(RawPixelsFilter(draw.oval(13, 13, 1, False)))
        self.sprites.append(self.oval)

        self.oval = core.Sprite(x=50, y=59)
        self.oval.filters.append(RawPixelsFilter(draw.oval(13, 13, 1, True)))
        self.sprites.append(self.oval)

        
        # draws every sprites
        for sprite in self.sprites:
            self.plot_sprite(sprite)
        
        # plots the virtual screen in the terminal emulator
        self.draw()


if __name__ == "__main__":
    try:
        DrawOval().run()
    except KeyboardInterrupt:   # handle key-interrupt
        DrawOval().quit()

