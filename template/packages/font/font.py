import pygame
from pygame.locals import *

import packages.value.variables as vars

class Font:
  def __init__(self, font_data):
    self.font_data = font_data

  def load(self):
    for key, f in self.font_data.items():
      f.loader().load(f.image_key, f.image_filename, f.keys, f.points, f.dim)

  # These static methods may benefit from being in their own Character class
  @staticmethod
  def add_character(key, character):
    vars.text_characters[key] = character

  @staticmethod
  def get_width(key):
    # Not too sure why this magic number works...
    # Could be cos of the 1px gap in the fontsheet
    return vars.text_characters[key].character.get_width() + 1

  @staticmethod
  def get_height(key):
    return vars.text_characters[key].character.get_height()

class FontDatum():
  def __init__(self, image_key, image_filename, keys, dim, loader):
    self.image_key = image_key,
    self.image_filename = image_filename

    keys_and_points = self._get_keys_and_points(keys)
    self.keys = keys_and_points[0]
    self.points = keys_and_points[1]
    self.dim = dim
    self.loader = loader

  def _get_keys_and_points(self, string_keys):
    x = 0
    y = 0
    keys = []
    points = []
    for key in string_keys:
      for ch in key:
        keys.append(ch)
        points.append((x, y))
        x += 1
      x = 0
      y += 1

    return [keys, points]
