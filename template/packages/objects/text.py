import pygame
from pygame.locals import *

import packages.value.variables as vars

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.font.font import Font

class TextObject(ABC):
  def __init__(self, text, position, limit):
    self.position = position
    self.is_active = True
    self.limit = limit
    self.set_text(text)

  def set_text(self, text):
    # How many lines of text?
    lines = []
    start = 0
    end = self.limit
    while start < len(text):
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
