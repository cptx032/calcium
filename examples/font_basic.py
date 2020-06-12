# coding: utf-8

import os
import sys
from datetime import datetime

from calcium import core, filters


def local_path(file_name: str) -> str:
    """Return the relative path to some file."""
    return os.path.join(os.path.dirname(sys.argv[0]), file_name)


class MainApp(core.TerminalApplication):
    def __init__(self):
        # the idea here is to set a very high fps to see really how many
        # fps we have using the "last_fps" app property
        super().__init__(fps=100000)
        # we are using a timer to update the label only when it needs
        # because the font/text manipulation here is very slow
        self.timer = core.Timer()
        self.font = filters.FontUtils.get_font(
            local_path("Ultrapixel.ttf"), 16
        )
        self.text = (
            "basic text\njosemwarrior.itch.io/\nultrapixel-font".upper()
        )
        self.sprite: core.Sprite = core.Sprite(
            filters=[
                filters.RawImageFilter(
                    image=filters.FontUtils.get_image_from_text(
                        font=self.font, text=self.text,
                    )
                )
            ]
        )
        self.bind("q", lambda *args: self.quit())
        self.schedule_update()

    def schedule_update(self):
        self.update_time()
        self.timer.after(1, self.schedule_update)

    def update_time(self):
        self.sprite.filters = [
            filters.RawImageFilter(
                image=filters.FontUtils.get_image_from_text(
                    font=self.font,
                    text=self.text
                    + "\n"
                    + datetime.now().strftime("%H:%M:%S"),
                    align="center",
                )
            )
        ]

    def update(self):
        self.timer.tick()
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()


if __name__ == "__main__":
    MainApp().run()
