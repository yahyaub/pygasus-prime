import pygame
from pygame.locals import *

import packages.value.variables as vars

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.display.grid import Grid
from packages.font.font import Font
from packages.image.image import Image
from packages.value.constants import SCALE

class TextObject(ABC):
  def __init__(self, text, position, limit):
    self.position = position
    self.is_active = True
    self.limit = limit
    self.set_text(text)

  def set_text(self, text):
    new_line_markers = " .,;:-_=!?/\\"

    # How many lines of text?
    lines = []
    start = 0
    end = self.limit + 1
    while start < len(text):

      # Smart line endings
      while (not text[start:end][-1] in new_line_markers) and (end > start+1):
        end -= 1
      if len(text[start:end]) == 1:
        while (not text[start:end][-1] in new_line_markers) and (end < len(text)):
          end += 1

      lines.append(text[start:end])
      start = end
      end += self.limit

    # Set the lines of text
    self.text = []
    text_width = 0
    text_height = 0
    for line in lines:
      line_text = []
      line_width = 0
      line_height = 0
      for ch in line:
        ch_obj = vars.text_characters[ch]
        line_width += Font.get_width(ch) + ch_obj.horizontal_spacing
        line_height = max(line_height, Font.get_height(ch) + ch_obj.vertical_spacing)
        line_text.append(ch_obj)
      text_width = max(text_width, line_width)
      text_height += line_height
      self.text.append(line_text)
    self.image = pygame.Surface((text_width, text_height))
    self.box = CollisionBox(self, (0, 0))

  def resize(self, dimensions, spacing):
    for line in self.text:
      for chobj in line:
        dim_x = dimensions[0] * SCALE
        dim_y = dimensions[1] * SCALE
        chobj.character = Image.resize(chobj.character, (dim_x, dim_y))
        chobj.set_spacing(spacing, (dim_x, dim_y))

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def clear(self):
    pass

  @abstractmethod
  def draw(self):
    pass

class CharacterObject():
  def __init__(self, character, spacing, spacing_scaled):
    self.character = character
    self.horizontal_spacing = spacing[0]
    self.horizontal_spacing_scaled = spacing_scaled[0]

    self.vertical_spacing = spacing[1]
    self.vertical_spacing_scaled = spacing_scaled[1]

  def draw(self, canvas, position):
    canvas.blit(self.character, position)
    return (position[0] + self.horizontal_spacing_scaled, position[1])

  def set_spacing(self, spacing, dimensions):
    self.horizontal_spacing = spacing[0]
    self.horizontal_spacing_scaled = dimensions[0] + spacing[0]

    self.vertical_spacing = spacing[1]
    self.vertical_spacing_scaled = dimensions[1] + spacing[1]
