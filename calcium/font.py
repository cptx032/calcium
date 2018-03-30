from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import load_default

from calcium.core import CalciumSprite
from calcium.image import ImageSprite


class FontSprite(CalciumSprite):

    def __init__(self, *args, **kwargs):
        _text = kwargs.pop('text', '')
        self.__text = ''
        self.font = kwargs.pop('font', load_default())
        self.fill = kwargs.pop('fill', (255,))

        # I'm using a 1x1 image just to create a Draw instance to calculates
        # the size of final image
        self.__size_draw = Draw(Image.new('1', (1, 1)))
        super(FontSprite, self).__init__(*args, **kwargs)
        # initial creation of text sprite
        self.text = _text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if value != self.text:
            self.animations[self.animation_key][self.frame_index] = self.get_frame(value)
        self.__text = value

    def get_frame(self, text):
        """Return the frame of actual text."""
        image = Image.new('1', self.__size_draw.textsize(
            text, font=self.font))
        drawer = Draw(image)
        self.size = image.size
        drawer.text((0, 0), text, fill=self.fill, font=self.font)
        return ImageSprite.get_frame_from_image(image)
