# coding: utf-8

import time
import typing

import pytweening

from calcium import core


class Animation:
    def __init__(
        self,
        obj: core.ObservableSet,
        prop: str,
        _from: float,
        to: float,
        duration: float,
        on_start: typing.Union[typing.Callable, None] = None,
        on_end: typing.Union[None, typing.Callable] = None,
        loop: bool = False,
        reverse_on_end: bool = False,
        func: typing.Callable = pytweening.easeOutQuart,
    ):
        """Animate numeric properties.

        Arguments:
            - obj: an object with observable properties, in most cases: a
                sprite
            - prop: string with the property to animate
            - _from: the initial property value. the start of animation
            - to: the final property value. the end of animation
            - duration: in seconds. how many time must last the animation
            - on_start: a function to be called in the start of animation
            - on_end: a function to be called in the end of animation
            - loop: flag to indicate if, in the end of animation, the
                animation must start again.
            - reverse_on_end: flag to indicate if, in the end of animation,
                it must start again but reversing the _from and to attributes.
                This is usefull for seamless loop animations. This attribute
                only works when loop=True.
            - func: an easing function to change the property over time. The
                function must receive an number in range [0, 1] and return
                another value in range [0, 1]. Use pytweening lib functions.
        """
        self.obj: core.ObservableSet = obj
        self.prop: str = prop
        self._from: float = _from
        self.to: float = to
        self.duration: float = duration
        self.on_start: typing.Union[typing.Callable, None] = on_start
        self.on_end: typing.Union[None, typing.Callable] = on_end
        self.loop: bool = loop
        self.reverse_on_end: bool = reverse_on_end
        self.func: typing.Callable = func
        self._start_time: typing.Union[None, float] = None

    def start(self) -> None:
        if self.on_start:
            self.on_start()
        self._start_time = time.time()

    def stop(self) -> None:
        self._start_time = None

    def tick(self) -> None:
        """Must be called every frame to process the animation."""
        if self._start_time:
            now = time.time()
            x = (now - self._start_time) / self.duration
            if x < 1.0:
                self.obj[self.prop] = self.lerp(
                    self._from, self.to, x, func=self.func
                )
            else:
                self.stop()
                if self.on_end:
                    self.on_end()
                if self.loop:
                    if self.reverse_on_end:
                        _old_from: float = self._from
                        self._from = self.to
                        self.to = _old_from
                    self.start()

    @classmethod
    def lerp(cls, a, b, x, func):
        return a + ((b - a) * func(x))
