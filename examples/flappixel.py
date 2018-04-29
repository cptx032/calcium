from calcium.core import CalciumScene, CalciumSprite
from calcium.terminal import CalciumTerminal
from calcium.effects import InvertScreenEffect
from calcium.draw import rectangle


class MainScene(CalciumScene):
    def __init__(self, window):
        super(MainScene, self).__init__('mainscene', window)
        self.pixel = CalciumSprite(8, 16, animations={'d': [[0,0,1]]})
        self.sprites.append(self.pixel)

        self.rec = CalciumSprite(
            7, 0,
            animations={'d': [rectangle(5, 14, fill=True)]})
        self.sprites.append(self.rec)

        self.rec1 = CalciumSprite(
            31, 0,
            animations={'d': [rectangle(3, 8, fill=True)]})
        self.sprites.append(self.rec1)

        self.rec2 = CalciumSprite(
            0, 22,
            animations={'d': [rectangle(5, 10, fill=True)]})
        self.sprites.append(self.rec2)

        self.rec3 = CalciumSprite(
            31, 14,
            animations={'d': [rectangle(3, 18, fill=True)]})
        self.sprites.append(self.rec3)

        self.bind(CalciumTerminal.ARROW_UP_KEY, self._up, '+')
        self.bind(CalciumTerminal.ARROW_DOWN_KEY, self._down, '+')

    def _up(self):
        if self.pixel.y > 0:
            self.pixel.y -= 1

    def _down(self):
        if self.pixel.y < self.window.screen.height-1:
            self.pixel.y += 1

    def run(self):
        for rec in [self.rec, self.rec1, self.rec2, self.rec3]:
            rec.x -= 0.4
            if (rec.x + rec.width) <= 0:
                rec.x = self.window.screen.width
            if rec.touching(self.pixel) or self.pixel.touching(rec):
                self.window.quit()
                break

    def draw(self):
        super(MainScene, self).draw()
        InvertScreenEffect.process(self.window.screen)

if __name__ == '__main__':
    app = CalciumTerminal(center=True, width=32, fps=60)
    app.scenes['mainscene'] = MainScene(app)
    app.actual_scene_name = 'mainscene'
    app.mainloop()
