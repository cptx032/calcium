# coding: utf-8

import atexit
import os
import sys
import termios
import time
import typing


class Timer:
    def __init__(self):
        self.__schedule_funcs: typing.Dict[
            typing.Callable, typing.List[float]
        ] = dict()

    def after(self, seconds: float, func: typing.Callable) -> None:
        """Schedule a function to be runned at 'seconds' seconds."""
        self.__schedule_funcs[func] = [seconds, time.time()]

    def tick(self) -> None:
        to_delete: typing.List[typing.Callable] = list()
        to_run: typing.List[typing.Callable] = list()
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


class ObservableVar:
    """A observable variable. Any object can subscribe to changes."""

    def __init__(self, content: typing.Any = None):
        self.__content: typing.Any = content
        self.__after_write_binds: typing.List[typing.Callable] = []

    def bind(self, func: typing.Callable, trigger: bool = True) -> None:
        self.__after_write_binds.append(func)
        if trigger:
            func(self)

    def get(self) -> typing.Any:
        return self.__content

    def set(self, value: typing.Any, trigger: bool = True) -> None:
        self.__content = value
        if trigger:
            self.trigger_all()

    def trigger_all(self) -> None:
        for func in self.__after_write_binds:
            func(self)


class ObservableSet:
    """Automatically create observable variables to instances."""

    def __init__(self):
        self._properties: typing.Dict[str, ObservableVar] = {}

    def _check_existence(self, attr: str) -> None:
        if attr not in self._properties:
            self._properties[attr] = ObservableVar()

    def __getitem__(self, attr: str) -> typing.Any:
        self._check_existence(attr)
        return self._properties[attr].get()

    def __setitem__(self, attr: str, value: typing.Any) -> None:
        self._check_existence(attr)
        self._properties[attr].set(value)

    def bind_to_prop(
        self, attr: str, func: typing.Callable, trigger: bool = True
    ) -> None:
        self._check_existence(attr)
        self._properties[attr].bind(func, trigger)


class BaseFilter:
    def __init__(self):
        self.active: bool = True

    def get(self, pixels: typing.List[int]) -> typing.List[int]:
        raise NotImplementedError


class Sprite(ObservableSet):
    def __init__(
        self,
        filters: typing.List[BaseFilter] = list(),
        x: float = 0,
        y: float = 0,
    ):
        super(Sprite, self).__init__()
        self.filters: typing.List[BaseFilter] = list(filters)
        # self.x: float = x
        # self.y: float = y
        self["x"] = x
        self["y"] = y

    def get_pixels(self) -> typing.List[int]:
        last_pixels: typing.List[int] = list()
        for f in filter(lambda i: i.active, self.filters):
            last_pixels = f.get(last_pixels)
        return last_pixels


class Screen:
    """Represent a virtual screen of 0s and 1s."""

    FILLED: str = "█"
    TOP: str = "▀"
    BOTTOM: str = "▄"
    BLANK_CHAR: str = " "

    def __init__(self, width: int = 80, height: int = 48):
        self.width: int = width
        self.height: int = height
        assert (self.height % 2) == 0
        self.lines: typing.List[typing.List[int]] = []
        self.clear()

    def clear(self) -> None:
        self.__fill(0)

    def fill(self) -> None:
        self.__fill(1)

    def __fill(self, value: int) -> None:
        self.lines = []
        for li in range(self.height):
            line = []
            for ci in range(self.width):
                line.append(value)
            self.lines.append(line)

    def get_string_lines(self) -> typing.List[str]:
        # each \n is 2 pixels so offsety must be divided by 2
        lines: typing.List[str] = []
        for y in range(0, self.height, 2):
            line: str = ""
            for x in range(self.width):
                top: int = self.lines[y][x]
                bottom: int = self.lines[y + 1][x]
                if top and bottom:
                    line += Screen.FILLED
                elif not top and not bottom:
                    line += Screen.BLANK_CHAR
                elif top and not bottom:
                    line += Screen.TOP
                elif not top and bottom:
                    line += Screen.BOTTOM
            lines.append(line)
        return lines

    def get_string(self) -> str:
        return "\n".join(self.get_string_lines())

    def set_pixel(self, x: float, y: float, pixel: int) -> None:
        assert pixel in (0, 1), "'{}': invalid range".format(pixel)
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        self.lines[int(y)][int(x)] = pixel

    def plot_sprite(self, sprite: Sprite) -> None:
        pixels: typing.List[int] = sprite.get_pixels()
        for i in range(0, len(pixels), 3):
            self.set_pixel(
                x=sprite["x"] + pixels[i],
                y=sprite["y"] + pixels[i + 1],
                pixel=pixels[i + 2],
            )


class Bindable:
    """Allow bind functions to be runned by a key trigger."""

    def __init__(self):
        self.function_map: typing.Dict[
            typing.Tuple[int, ...], typing.List[typing.Callable]
        ] = {}
        self.any_function_list: typing.List[typing.Callable] = list()

    def bind(
        self, key, func: typing.Callable, op: typing.Union[str, None] = None,
    ):
        if op not in (None, "+", "-"):
            raise ValueError("Wrong operation")
        if type(key) is str and len(key) > 1:
            raise ValueError("The key must have only one character")

        if type(key) is not tuple:
            key = (ord(key),)

        if key is None:
            if op is None:
                self.any_function_list = [func]
            elif op == "+":
                self.any_function_list.append(func)
            elif op == "-":
                self.any_function_list.remove(func)
        else:
            if key not in self.function_map:
                self.function_map[key] = list()

            if op is None:
                self.function_map[key] = [func]
            elif op == "+":
                self.function_map[key].append(func)
            elif op == "-":
                self.function_map[key].remove(func)

    def trigger_key(self, key: typing.Tuple[int, ...]) -> None:
        for f in self.function_map.get(key, list()):
            f(key)
        for f in self.any_function_list:
            f(key)


class TerminalApplication(Bindable):
    ESCAPE_KEY: typing.Tuple[int, ...] = (27,)
    ENTER_KEY: typing.Tuple[int, ...] = (10,)
    ARROW_UP_KEY: typing.Tuple[int, ...] = (27, 91, 65)
    ARROW_DOWN_KEY: typing.Tuple[int, ...] = (27, 91, 66)
    ARROW_RIGHT_KEY: typing.Tuple[int, ...] = (27, 91, 67)
    ARROW_LEFT_KEY: typing.Tuple[int, ...] = (27, 91, 68)

    def __init__(
        self,
        width: int = 80,
        height: int = 48,
        center: bool = False,
        terminal_size: bool = False,
        fps: int = 24,
    ):
        super().__init__()
        (
            available_width,
            available_height,
        ) = TerminalApplication.get_terminal_size_in_pixels()
        self.stop: bool = False
        if terminal_size:
            width, height = available_width, available_height
        else:
            if width > available_width:
                raise ValueError(
                    "Width cant be greater than {}".format(available_width)
                )
            if height > available_height:
                raise ValueError(
                    "Height cant be greater than {}".format(available_height)
                )

        self.screen: Screen = Screen(width=width, height=height)
        self.fps: int = fps
        self.center: bool = center
        self._frame_counter: int = 0
        self.last_fps: int = 0
        self._fps_start_time: float = time.time()

        self.old_terminal_settings: typing.Any = None
        self.new_terminal_settings: typing.Any = None
        self.init_any_key()
        self.go_to_0_0()
        self.blank_terminal()
        self.hide_cursor()
        atexit.register(self.restore_terminal)

    @property
    def width(self) -> int:
        return self.screen.width

    @property
    def height(self) -> int:
        return self.screen.height

    def set_pixel(self, *args):
        """Alias."""
        self.screen.set_pixel(*args)

    def plot_sprite(self, *args):
        """Alias."""
        self.screen.plot_sprite(*args)

    def init_any_key(self):
        self.old_terminal_settings = termios.tcgetattr(sys.stdin)
        self.new_terminal_settings = termios.tcgetattr(sys.stdin)
        self.new_terminal_settings[3] = self.new_terminal_settings[3] & ~(
            termios.ECHO | termios.ICANON
        )
        self.new_terminal_settings[6][termios.VMIN] = 0
        self.new_terminal_settings[6][termios.VTIME] = 0
        termios.tcsetattr(
            sys.stdin, termios.TCSADRAIN, self.new_terminal_settings
        )

    def restore_terminal(self) -> None:
        sys.stdout.write("\033[0m")
        self.show_cursor()
        if self.old_terminal_settings:
            termios.tcsetattr(
                sys.stdin, termios.TCSADRAIN, self.old_terminal_settings
            )

    def hide_cursor(self) -> None:
        sys.stdout.write("\033[?25l")

    def show_cursor(self) -> None:
        sys.stdout.write("\033[?25h")

    def blank_terminal(self) -> None:
        sys.stdout.write("\033[0J")

    @staticmethod
    def get_terminal_size_in_pixels() -> typing.Tuple[int, int]:
        size = os.get_terminal_size()
        width, height = size.columns, size.lines
        return (width, height * 2)

    def update(self) -> None:
        """Contains the main logic of application."""
        raise NotImplementedError("Main logic method must be implemented")

    def run(self) -> None:
        """Start the main while loop for event processing and app logic."""
        while not self.stop:
            self.process_next_frame()

    def process_next_frame(self) -> None:
        """Run one tick of application."""
        start: float = time.time()
        self.process_input()
        self.update()
        elapsed_time = time.time() - start
        sleep_time = (1.0 / self.fps) - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

        # calculating how many frames per seconds
        self._frame_counter += 1
        if (time.time() - self._fps_start_time) >= 1:
            self.last_fps = self._frame_counter
            self._frame_counter = 0
            self._fps_start_time = time.time()

    def process_input(self) -> None:
        key = self.anykey()
        if key:
            self.trigger_key(key)

    def anykey(self) -> typing.Tuple[int, ...]:
        ch_set = []
        ch = os.read(sys.stdin.fileno(), 1)
        while ch is not None and len(ch) > 0:
            # in python3 ch[0] is in anteger
            c = chr(ch[0])
            ch_set.append(ord(c))
            ch = os.read(sys.stdin.fileno(), 1)
        return tuple(ch_set)

    def go_to_0_0(self):
        # go to (0, 0) position
        sys.stdout.write("\033[0;0H")

    def clear(self):
        self.screen.clear()
        self.go_to_0_0()

    def fill(self):
        self.screen.fill()
        self.go_to_0_0()

    def draw(self) -> None:
        """Plot the content of virtual screen in the terminal emulator."""
        if self.center:
            raise NotImplementedError
        else:
            sys.stdout.write(self.screen.get_string())
            sys.stdout.flush()

    def quit(self):
        """Stop the main processing."""
        self.stop = True

    def set_fg_color(self, r, g, b):
        sys.stdout.write("\033[38;2;{};{};{}m".format(r, g, b))

    def set_bg_color(self, r, g, b):
        sys.stdout.write("\033[48;2;{};{};{}m".format(r, g, b))


if __name__ == "__main__":

    class MyApp(TerminalApplication):
        def __init__(self):
            self.x = 0
            self.y = 0
            super(MyApp, self).__init__()
            self.bind("q", lambda *args: self.quit(), "+")

        def update(self):
            self.clear()
            self.set_pixel(self.x, self.y, 1)
            self.draw()

            self.x += 1
            if self.x >= self.screen.width:
                self.x = 0
                self.y += 1
                if self.y >= self.screen.height:
                    self.y = 0

    MyApp().run()
