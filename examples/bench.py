from random import randint as ri
import sys

from calcium.core import CalciumScene, CalciumSprite
from calcium.draw import rectangle
from calcium.terminal import CalciumTerminal

REC_NUM = 100

if '-num' in sys.argv:
    REC_NUM = int(sys.argv[sys.argv.index('-num') + 1])


class MainScene(CalciumScene):
    def __init__(self, app):
        super(MainScene, self).__init__('main', app)
        for i in range(REC_NUM):
            rec_size = ri(10, 20)
            sprite = CalciumSprite(
                ri(0, app.screen.width), ri(0, app.screen.height),
                animations={'default': [rectangle(rec_size, rec_size)]})
            self.sprites.append(sprite)

    def run(self):
        # fixme: put them to rotate and compare with PIL rotate
        pass


if __name__ == '__main__':
    app = CalciumTerminal(terminal_size=True)
    app.add_scene(MainScene(app))
    app.mainloop()
    print(app.last_fps)
