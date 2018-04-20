# coding: utf-8

import copy
import time

import calcium.utils as utils


class CalciumSprite:
    def __init__(
            self, x, y,
            animations, frame_index=0,
            animation_key=None,
            size=None, visible=True):
        self.x = x
        self.y = y
        self.visible = visible
        self.animations = animations
        self.animation_key = animation_key or list(animations.keys())[0]
        self.frame_index = frame_index
        self.size = size
        if not size:
            self.size = CalciumSprite.get_size_from_pixels(
                self.get_pixels())

    def is_touching(self, sprite):
        if self.x > (sprite.x + sprite.size[0]):
            return False
        if sprite.x > (self.x + self.size[0]):
            return False
        if self.y > (sprite.y + sprite.size[1]):
            return False
        if sprite.y > (self.y + self.size[1]):
            return False
        return True

    @staticmethod
    def get_size_from_pixels(pixels):
        width = 0
        height = 0
        for i in range(0, len(pixels), 3):
            x = pixels[i]
            y = pixels[i + 1]
            if x > width:
                width = x
            if y > height:
                height = y
        # cause coordenates starts in (0, 0) we must
        # sum 1
        return (width + 1, height + 1)

    def align(self, anchor, x, y):
        offsetx = -self.size[0] * anchor[0]
        offsety = -self.size[1] * anchor[1]
        self.x = x + offsetx
        self.y = y + offsety

    def get_pixels(self):
        return self.animations.get(self.animation_key)[self.frame_index]

    def next_frame(self):
        self.frame_index += 1
        if self.frame_index >= len(self.animations.get(self.animation_key)):
            self.frame_index = 0

    def last_frame(self):
        self.frame_index -= 1
        if self.frame_index < 0:
            self.frame_index = len(self.animations.get(self.animation_key)) - 1

    def clone(self):
        return copy.deepcopy(self)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def nw(self):
        return [self.x, self.y]

    @property
    def sw(self):
        return [self.x, self.y + self.height]

    @property
    def ne(self):
        return [self.x + self.width, self.y]

    @property
    def se(self):
        return [self.x + self.width, self.y + self.height]

    def is_inside(self, x, y):
        u"""Verify if point (x y) is inside the sprite 'self'."""
        inx = x < (self.x + self.width) and x > self.x
        if not inx:
            return False
        return y < (self.y + self.height) and y > self.y

    def touching(self, sprite):
        u"""Return True if 'self' i touching 'sprite'."""
        nw = sprite.is_inside(*self.nw)
        sw = sprite.is_inside(*self.sw)
        ne = sprite.is_inside(*self.ne)
        se = sprite.is_inside(*self.se)
        return nw or sw or ne or se

    # def t_left(self, sprite):
    #     u"""Return True if 'self' is touching your left side."""
    #     return sprite.point_inside(sprite.nw) or sprite.point_inside(self.sw)

    # def t_right(self, sprite):
    #     u"""Return True if 'self' is touching your right side."""
    #     return sprite.point_inside(self.ne) or sprite.point_inside(self.se)

    # def t_down(self, sprite):
    #     u"""Return True if 'self' is touching your down side."""
    #     return sprite.point_inside(self.sw) or sprite.point_inside(self.se)

    # def t_up(self, sprite):
    #     u"""Return True if 'self' is touching your up side."""
    #     return sprite.point_inside(self.nw) or sprite.point_inside(self.ne)

    @staticmethod
    def get_frame_from_image(image_path):
        from PIL import Image
        image = Image.open(image_path)
        frame = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                frame.extend([x, y, utils.get_gray(image, x, y)])
        return frame

    def add_frame_from_image(self, image_path):
        self.animations[self.animation_key].append(
            self.get_frame_from_image(image_path))


class CalciumScreen:
    FILLED = u'█'
    TOP = u'▀'
    BOTTOM = u'▄'
    BLANK_CHAR = u' '

    def __init__(self, width, height=None, offsetx=0, offsety=0):
        u"""Represent a virtual screen."""
        self.offsetx = offsetx
        self.offsety = offsety
        self.width = width
        self.height = height or width
        assert (self.height % 2) == 0
        self.lines = []
        self.clear()

    def clear(self):
        self.__fill(0)

    def fill(self):
        self.__fill(1)

    def __fill(self, value):
        self.lines = []
        for li in range(self.height):
            line = []
            for ci in range(self.width):
                line.append(value)
            self.lines.append(line)

    def get_string(self):
        # each \n is 2 pixels so offsety must be divided by 2
        r = '\n' * int(self.offsety / 2)
        for y in range(0, self.height, 2):
            r += ' ' * self.offsetx
            for x in range(self.width):
                top = self.lines[y][x]
                bottom = self.lines[y + 1][x]
                if top and bottom:
                    r += CalciumScreen.FILLED
                elif not top and not bottom:
                    r += CalciumScreen.BLANK_CHAR
                elif top and not bottom:
                    r += CalciumScreen.TOP
                elif not top and bottom:
                    r += CalciumScreen.BOTTOM
            if y <= self.height:
                r += u'\n'
        return r[:-1]

    def __repr__(self):
        return self.get_string()

    def pixel(self, x, y, pixel):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        self.lines[int(y)][int(x)] = pixel

    def plot(self, sprite):
        if not sprite.visible:
            return
        pixels = sprite.get_pixels()
        for i in range(0, len(pixels), 3):
            self.pixel(
                sprite.x + pixels[i],
                sprite.y + pixels[i + 1],
                pixels[i + 2]
            )


class Timer:
    def __init__(self):
        self.__schedule_funcs = dict()

    def after(self, seconds, func):
        """Schedule a function to be runned at 'seconds' seconds."""
        self.__schedule_funcs[func] = [seconds, time.time()]

    def tick(self):
        to_delete = list()
        to_run = list()
        for function, time_info in self.__schedule_funcs.items():
            if time.time() - time_info[1] >= time_info[0]:
                to_run.append(function)
                to_delete.append(function)
        # we need to delete the functions before
        # run the functions for situation in which
        # the function call .after scheduling
        # it self
        for k in to_delete:
            del self.__schedule_funcs[k]
        for func in to_run:
            func()


class CalciumScene:
    def __init__(self, name, window):
        self.name = name
        self.window = window
        self.sprites = list()
        self.function_map = dict()
        self.timer = Timer()

        self.bind('q', window.quit, '+')

    def run(self):
        """The main logic of scene. Is called once per frame."""
        self.timer.tick()

    def draw(self):
        """Used to plot all sprite in screen."""
        for sprite in self.sprites:
            self.window.screen.plot(sprite)

    def bind(self, key, func, op=None):
        """Bind a function to be called when pressing a key."""
        assert op in (None, '+', '-'), ValueError
        if type(key) != tuple:
            key = (ord(key), )
        if not self.function_map.get(key):
            self.function_map[key] = list()
        if not op:
            self.function_map[key] = list()
        list_operation = self.function_map[key].append
        if op == '-':
            list_operation = self.function_map[key].remove
        list_operation(func)

    def __repr__(self):
        return self.name


class GenericWindow:
    def __init__(self, width, height=None,
                 offsetx=0, offsety=0, fps=60):
        self.fps = fps
        self.keep_running = True

        self.last_fps = None
        self.__frame_counter = 0
        self.__fps_start_time = time.time()

        self.screen = CalciumScreen(
            width, height, offsetx=offsetx, offsety=offsety)
        self.scenes = dict()
        self.actual_scene_name = None

    @property
    def scene(self):
        u"""Return the actual scene instance."""
        return self.scenes[self.actual_scene_name]

    def add_scene(self, scene, activate=True):
        u"""Helper to add a scene to app."""
        self.scenes[scene.name] = scene
        if activate:
            self.actual_scene_name = scene.name

    def quit(self):
        u"""Stop the mainloop of game."""
        self.keep_running = False

    def next_frame(self):
        u"""Process one frame completely."""
        start = time.time()
        self.process_input()
        self.run()
        elapsed_time = time.time() - start
        sleep_time = (1.0 / self.fps) - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

        # calculating how many frames per seconds
        self.__frame_counter += 1
        if (time.time() - self.__fps_start_time) >= 1:
            self.last_fps = self.__frame_counter
            self.__frame_counter = 0
            self.__fps_start_time = time.time()

    def bind(self, key, func, op=None):
        u"""Bind a function to be called when pressing a key.

        This function is binded to actual scene
        """
        return self.scene.bind(key, func, op)

    def process_input(self):
        u"""Function used to receive and process events."""
        raise NotImplemented

    def run(self):
        u"""Function that is called every frame in mainloop.

        Basically it run the 'run' function of scene, clear the
        screen and then plot all sprites
        """
        self.screen.clear()
        self.scene.run()
        self.scene.draw()

        self.clear()
        self.draw()

    def draw(self):
        u"""Function the plot the screen string in window."""
        raise NotImplemented

    def clear(self):
        u"""Function used to clear the implemented window."""
        raise NotImplemented

    def set_fg_color(self):
        u"""Function used to change the font color."""
        raise NotImplemented

    def set_bg_color_rgb(self):
        u"""Function used to change the background color."""
        raise NotImplemented
