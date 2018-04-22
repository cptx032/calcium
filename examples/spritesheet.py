from calcium import core
from calcium import effects
from calcium import image
from calcium import terminal
from calcium import utils


class MainScene(core.CalciumScene):
    def __init__(self, window):
        super(MainScene, self).__init__('main', window)
        self.character = core.CalciumSprite(
            10, self.window.screen.height - 16,
            dict(
                normal=image.ImageSprite.get_frames_from_sheet(
                    utils.local_path('sheet.png'), 6, 1)))
        self.sprites.append(self.character)
        self.bind('q', self.window.quit, '+')
        self.counter = 0.0

    def run(self):
        self.counter += 1
        if self.counter >= 5:
            self.character.next_frame()
            self.counter = 0

    def draw(self):
        super(MainScene, self).draw()
        effects.BorderScreenEffect.process(self.window.screen)
        # when the terminal is in fullscreen/maximized the invert
        # effect decrease the fps cause its looping all screen
        # fixme: think a way to solve this
        effects.InvertScreenEffect.process(self.window.screen)


class SpriteSheetApp(terminal.CalciumTerminal):
    def __init__(self, *args, **kwargs):
        terminal.CalciumTerminal.__init__(self, *args, **kwargs)
        self.add_scene(MainScene(self))

        self.set_bg_color(0, 0, 0)
        self.set_fg_color_rgb('839495')


if __name__ == '__main__':
    SpriteSheetApp(terminal_size=True, center=True).mainloop()
