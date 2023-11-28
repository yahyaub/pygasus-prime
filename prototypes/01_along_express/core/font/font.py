import pygame
from pygame.locals import *

from core.value.constants import SCORE_KEYS, SCORE_DIM

from packages.font.font import Font, FontDatum
from packages.image.spritesheet import Fontsheet

class MyFont(Font):
  def __init__(self):
    font_data = {
      # key: FontDatum(key, image_filename, key_list, key_dim, fontsheet)
      "score_font": FontDatum("score_datum", "numbers_all.png", SCORE_KEYS, SCORE_DIM, ScoreFontsheet)
    }

    super().__init__(font_data)

'''
Define fontsheets for different fontsheets!

class MyFontsheet(Fontsheet):
  def __init__(self):
    super().__init__(character_spacing (in px))
'''

class ScoreFontsheet(Fontsheet):
  def __init__(self):
    super().__init__(SCORE_DIM[0] * 4.5)
