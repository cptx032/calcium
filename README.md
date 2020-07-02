# Calcium

<p align="center">
  <img src="docs/calcium.gif?raw=true" alt="example-01-running"/>
</p>

Calcium is a python 3 library to build **games** (or interactive applications) in **terminal emulators**. It works by creating a "Calcium Screen" that represents a virtual screen filled with 0s and 1s and plotting this virtual screen to the terminal emulator.

# Learning the basics

## Main Concepts

Every calcium application must inherits from `core.TerminalApplication` and override the function `update`. The `update` is the function that is called in every single frame. So let's look how we can plot a single pixel in the screen:


```python
from calcium import core

class HelloWorldApp(core.TerminalApplication):
    def update(self):
        self.clear()
        self.set_pixel(2, 2, 1)
        self.draw()


if __name__ == "__main__":
    HelloWorldApp.run()
```

<p align="center">
  <img src="docs/example-01.png?raw=true" alt="example-01-running"/>
</p>

The `TerminalApplication` has a property called `screen`. It represents a virtual screen and all drawing that we can do is made in this virtual screen.
On every frame we can draw on this virtual screen and then plot this virtual screen in the terminal. The `clear` method clears the virtual screen and clears the terminal emulator screen. The `set_pixel` call draws a pixel in the (2, 2) coordinate, in the virtual screen, and finally, the `draw` method plot the virtual screen to the terminal emulator screen.

The virtual screen, in the most cases, don't need to be accessed directly, but you can do it if you want. Just do:

```python
# setting the upper left corner to 1 (filled)
def update(self):
    ...
    self.screen.lines[0][0] = 1
    ...
```


## Sprites and Filters

A sprite is a collection of pixels arranged around a point/coordinate. The point/coordinate we can call "origin" or "position" of the sprite. We use functions called "filters" to determine the pixel data binded to the sprite. The pixels data returned from filters must be in the format `x, y, (1 or 0)`. So, if we a have a sprite in the position (10, 10) and it have only one white pixel, located in the same sprite's origin point, the pixel data returned from one filter must be: `[0, 0, 1]`, if the sprite have two pixels, one in the origin point and other next to it, in your right side, the pixel data returned by the filter will be: `[0, 0, 1, 1, 0, 1]`. Every time we move the sprite in the virtual screen the points will be moved together. Let's see an example of an sprite with three pixels, one black pixel in between two white pixels:


```python
from calcium import core

class MySpritePixelsFilter(core.BaseFilter):
    def get(self, pixels):
        return [
            0, 0, 1,
            1, 0, 0,
            2, 0, 1,
        ]

class MyApp(core.TerminalApplication):
    def __init__(self):
        super().__init__()
        self.sprite = core.Sprite(filters=[
            MySpritePixelsFilter()
        ])

    def update(self):
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()

MyApp().run()
```

<p align="center">
  <img src="docs/example-02.png?raw=true" alt="example-02-running"/>
</p>

You probably noted the used of `plot_sprite` method. It do just what are thinking! It draw the points returned by all the filters of the sprite in the virtual screen.

Why we use filters to set the sprite's pixels? Because we can arrange filters one next to other to create a chain of effects! This is a try to make a more flexible sprite effects design. For example, we can create a filter that creates randomically pixels data, and next to it, append another filter that takes the pixels returned by the last filter and proccess it, making a border around the pixels, or inverting the colors of last filters, or making the pixels show/hide periodically, making it flash...many possibilities!

This is why, in the example above, the method `get` of our `MySpritePixelsFilter` receive a `pixels` argument. This argument stores the pixels returned by the last filter.

So let's try some default filter to you understand the power of them:


```python
from calcium import core
from calcium import filters
class MyApp(core.TerminalApplication):
    def __init__(self):
        super().__init__()
        self.sprite = core.Sprite(filters=[
            filters.RawImageFilter(image_path="./lenna.png"),
            filters.InvertFilter(),
        ])

    def update(self):
        self.clear()
        self.plot_sprite(self.sprite)
        self.draw()

MyApp().run()
```

Above you can see two filters working together. The first takes one image, converts to black/white and the next one takes the pixels returned by the last filter and invert its colors.

<p align="center">
  <img src="docs/example-03.png?raw=true" alt="example-03-running"/>
</p>

Note that the order of filters is very important, if we invert the filters order in the example above, making the invert filters first, the image will be shown without any effect. This will happen because the invert filter will receive none pixels (because before it doesn't exist any filter) and than we will include an filter that just ignores the last pixel data. This one thing to pay attention when working with filters, you will need to know if it uses the last pixel data or just ignores it. Below we have the list of default filters available:

#### filters.InvertFilter
Invert the colors of last pixels

#### filters.BoundsFilter
Do nothing with the pixels. Just receive them and return them back. This filter is used to calculate the width/height os sprite and create dinamic properties in the sprite. This is used basically for alignment or physics.

#### filters.RawImageFilter
Ignores the last pixels, so you want to use this filter in the beginning of filters list. It receives a PIL.Image instance or a file path with the image. Note that the image will not be resized when using this filter, so, use images already resized.

#### filters.SpriteSheetFilter
Ignores the last pixels, so you want to use this filter in the beginning of filters list. It receives a list of PIL.Image instances and switch them in the time making animations.

#### filters.PlatformPhysicsFilter
Do nothing with the pixels. Just receive them and return them back.
This filter is used to make objects interacts with others. This is meant to a very basic platform games.


## Sprite observable properties
TODO

## Timers
TODO

## Scenes
TODO

## Sounds
TODO

## Animation
TODO

## How I can help
- create cool filters
- do improvements in the CI (because is not set yet :p )
- CREATE GAMES!

## Games powered by Calcium

- include a game here please...
