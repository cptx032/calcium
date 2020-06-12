# coding: utf-8

from calcium import animation, core, filters


class MyApp(core.TerminalApplication):
    def __init__(self):
        super().__init__(terminal_size=True, fps=24)

        self.sprite = core.Sprite(
            filters=[filters.RawPixelsFilter(pixels=[0, 0, 1])],
            x=self.width / 2,
            y=self.height / 2,
        )

        self.anim = animation.Animation(
            obj=self.sprite,
            prop="x",
            _from=(self.width / 2) - 20,
            to=(self.width / 2) + 20,
            duration=0.5,
            loop=True,
            reverse_on_end=True,
        )
        self.anim.start()

        self.bind("q", lambda *args: self.quit())

    def update(self):
        self.anim.tick()
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()


if __name__ == "__main__":
    MyApp().run()
