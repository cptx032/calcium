# coding: utf-8


import typing

from calcium import core


# fixme > scene filters
# fixme > scene offset
class Scene(core.Bindable):
    def __init__(
        self,
        app: core.TerminalApplication,
        sprites: typing.Union[None, typing.List[core.Sprite]] = None,
        active: bool = True,
    ):
        """Represent a scene with multiple sprites.

        A scene is a collection of sprite with its own events. The events
        must be binded to the scene instead of the application.

        Arguments:
            - app: a reference to the terminal application with the virtual
                screen
            - sprites: a list of sprites. They can be set on the startup
                of scene already, but you can gradually add new sprites to the
                scene just calling 'scene_instance.sprites.append()'. As
                sprite attribute its just a list, you can reorder/sort, remove
                sprites etc
            - active: a flag that indicates if the scene must be processed
                or not in such way that you can add the scene to a scene list
                but flag it to not be processed
        """
        self.app: core.TerminalApplication = app
        self.sprites: typing.List[core.Sprite] = sprites or list()
        self.active: bool = active
        super().__init__()

    def update(self):
        """Draw the sprites."""
        if not self.active:
            return
        for sprite in self.sprites:
            self.app.plot_sprite(sprite)


class SceneApplication(core.TerminalApplication):
    """Scene manager. Allow switch/enable/disable scenes."""

    def __init__(self, *args, **kwargs):
        self.scenes: typing.List[Scene] = list()
        super().__init__(*args, **kwargs)

    def update(self):
        self.clear()
        for scene in self.scenes:
            scene.update()
        self.draw()

    def trigger_key(self, *args, **kwargs):
        # redirecting the events to scenes
        scenes: typing.List[Scene] = list(
            filter(lambda i: i.active, self.scenes)
        )
        for scene in scenes:
            scene.trigger_key(*args, **kwargs)


if __name__ == "__main__":
    from calcium import draw

    class RawFilter(core.BaseFilter):
        def __init__(self, pixels: typing.List[int]):
            self._pixels = pixels

        def get(self, pixels):
            return self._pixels

    class LineScene(Scene):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sprite = core.Sprite(
                filters=[RawFilter(draw.line(0, 0, 10, 0))], x=10, y=10
            )
            self.sprites.append(self.sprite)
            self.bind("q", lambda *args: self.app.quit())
            self.bind("x", lambda *args: self.x_to_move_left())

        def x_to_move_left(self):
            self.sprite.x -= 1

    class SquareScene(Scene):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sprite = core.Sprite(
                filters=[RawFilter(draw.rectangle(10, 10))], x=20, y=20
            )
            self.sprites.append(self.sprite)
            self.bind("q", lambda *args: self.app.quit())

        def update(self, *args, **kwargs):
            return super().update(*args, **kwargs)

    class MainApp(SceneApplication):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.line_scene = LineScene(app=self)
            self.square_scene = SquareScene(app=self, active=False)
            self.scenes.append(self.line_scene)
            self.scenes.append(self.square_scene)

            self.line_scene.bind("n", lambda *args: self.toggle_scene())
            self.square_scene.bind("n", lambda *args: self.toggle_scene())

        def toggle_scene(self):
            self.line_scene.active = not self.line_scene.active
            self.square_scene.active = not self.square_scene.active

    app = MainApp()
    app.run()
