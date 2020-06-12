# coding: utf-8


import pytest

from calcium.core import BaseFilter, Screen, Sprite


def test_new_sprite_creation():
    sprite = Sprite()
    assert sprite.get_pixels() == []


def test_wrong_screen_size():
    with pytest.raises(AssertionError):
        Screen(width=1, height=1)


def test_get_string():
    screen = Screen(width=1, height=4)
    assert screen.get_string() == " \n "
    screen.fill()
    assert screen.get_string() == Screen.FILLED + "\n" + Screen.FILLED
    screen.clear()
    assert screen.get_string_lines() == [" ", " "]


def test_set_pixel():
    screen = Screen(width=1, height=4)
    screen.set_pixel(0, 0, 1)
    assert screen.get_string_lines() == [Screen.TOP, " "]
    screen.set_pixel(0, 1, 1)
    assert screen.get_string_lines() == [Screen.FILLED, " "]


def test_sprite_plot():
    class RawImageFilter(BaseFilter):
        def get(self, pixels):
            return [0, 0, 1]

    screen = Screen(width=1, height=4)
    sprite = Sprite(filters=[RawImageFilter()])
    screen.plot_sprite(sprite)
    assert screen.get_string_lines() == [Screen.TOP, " "]


def test_observable_var():
    sprite = Sprite()
    assert sprite["light_color"] == None
    sprite["light_color"] = 1
    assert sprite["light_color"] == 1


def test_observable_bind():
    def mark_as_called(prop):
        prop.set(3, trigger=False)

    sprite = Sprite()
    sprite["light_color"] = 1
    sprite.bind_to_prop("light_color", mark_as_called, trigger=False)
    assert sprite["light_color"] == 1
    sprite["light_color"] = 2
    assert sprite["light_color"] == 3
