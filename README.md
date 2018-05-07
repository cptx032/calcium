# calcium

Calcium is a python 3 library to build **games** (or interactive applications) in **linux terminals** (or any text-device). It works by creating a "CalciumScreen" that represents a virtual screen filled with 0s and 1s. You can use it to plot the text in any place you want.

<p align="center">
  <img src="screenshots/flappixel.gif?raw=true" alt="flappixel"/>
</p>

<p align="center">
  <img src="screenshots/runner.gif?raw=true" alt="runner"/>
</p>

### Hello World
```python
from calcium.terminal import CalciumTerminal
from calcium.core import CalciumScene

if __name__ == '__main__':
    app = CalciumTerminal(terminal_size=True)
    app.add_scene(CalciumScene('mainscene', app))
    app.mainloop()
```

The code above does actually..nothing. Just a blank screen.


## Technical details

A "pixel" in this virtual screen has only two values: 0 and 1. The pixel 1 is mapped to a "filled" character, and 0 is mapped to a blank character.

Calcium uses four characters to transform a virtual screen to
a string:

```python
FILLED = u'█'
TOP = u'▀'
BOTTOM = u'▄'
BLANK_CHAR = u' '
```

Because a character is naturally "vertical" calcium splits it in two. So, each character represents two pixel, one in top of other. This is why every virtual screen must have an even number height.

m3x6 font - https://managore.itch.io/m5x7
