from datetime import datetime

from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from calcium.core import CalciumSprite
from calcium.image import ImageSprite
from calcium.terminal import CalciumTerminal


class ClockApp(CalciumTerminal):
    def __init__(self, *args, **kwargs):
        super(ClockApp, self).__init__(*args, **kwargs)
        self.bind('q', self.quit, '+')
        self.font = truetype('verdana', 10)

    def run(self):
        now = datetime.now()
        text = '{}:{}:{}'.format(
            str(now.hour).zfill(2), str(now.minute).zfill(2),
            str(now.second).zfill(2))
        i = Image.new('1', (80, 48))
        draw = Draw(i)
        draw.text((0, 0), text, fill=(255,), font=self.font)

        frame = ImageSprite.get_frame_from_image(i)
        sprite = CalciumSprite(0, 0, {
            'normal': [frame]
        })
        sprite.align((0.5, 0.5), 40, 24)
        self.screen.clear()
        self.screen.plot(sprite)
        self.go_to_0_0()
        self.draw()


if __name__ == '__main__':
    app = ClockApp(terminal_size=True, fps=1)
    app.mainloop()
    print(app.last_fps)
