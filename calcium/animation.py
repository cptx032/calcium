import pytweening
import time


def interpolation(a, b, x, func):
    return a + ((b - a) * func(x))


class Animation:
    """Animation object."""

    def __init__(
            self, obj, prop, _from, to, duration,
            on_start=None, on_end=None, loop=False,
            reverse_on_end=False, func=pytweening.easeOutQuart):
        self.obj = obj
        self.prop = prop
        self._from = _from
        self.to = to
        self.duration = duration
        self._start_time = None
        self.on_start = on_start
        self.on_end = on_end
        self.loop = loop
        self.reverse_on_end = reverse_on_end
        self.func = func

    def start(self):
        if self.on_start:
            self.on_start()
        self._start_time = time.time()

    def stop(self):
        self._start_time = None

    def tick(self):
        """Must be called every frame to process the animation."""
        if self._start_time:
            now = time.time()
            x = (now - self._start_time) / self.duration
            if x < 1.0:
                setattr(
                    self.obj,
                    self.prop,
                    interpolation(self._from, self.to, x, func=self.func))
            else:
                self.stop()
                if self.on_end:
                    self.on_end()
                if self.loop:
                    if self.reverse_on_end:
                        _old_from = self._from
                        self._from = self.to
                        self.to = _old_from
                    self.start()
