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

        for i in range(15):
            self.oval = core.Sprite(x=50-(i*5), y=50-(i*5))
            self.oval.filters.append(RawPixelsFilter(draw.oval(10+(i*10), 10+(i*10), 1, False)))
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

