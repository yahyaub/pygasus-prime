import pygame
from pygame.locals import *

from core.value.constants import FONT_DIM, FONT_SPACE, FONT_KEYS
from packages.font.font import Font, FontDatum
from packages.image.spritesheet import Fontsheet

class MyFont(Font):
  def __init__(self):
    font_data = {
      # key: FontDatum(key, image_filename, key_list, key_dim, fontsheet)
      "sample_font": FontDatum("sample_font", "sample_font_white.png", FONT_KEYS, FONT_DIM, SampleFontsheet)
    }

    super().__init__(font_data)

'''
Define fontsheets for different fontsheets!

class MyFontsheet(Fontsheet):
  def __init__(self):
    super().__init__(character_spacing (in px))
'''

class SampleFontsheet(Fontsheet):
  def __init__(self):
    super().__init__(FONT_DIM, FONT_SPACE)