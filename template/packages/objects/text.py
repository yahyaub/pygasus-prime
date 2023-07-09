import pygame
from pygame.locals import *

import packages.value.variables as vars

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.font.font import Font

class TextObject(ABC):
  def __init__(self, text, position):
    self.position = position
    self.is_active = True
    self.set_text(text)

  def set_text(self, text):
    self.text = []
    width = 0
    height = 0
    for ch in text:
      width += Font.get_width(ch)
      height = max(height, Font.get_height(ch))
      self.text.append(vars.text_characters[ch])
    self.image = pygame.Surface((width, height))
    self.box = CollisionBox(self)

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
  def __init__(self, character, spacing):
    self.character = character
    self.spacing = spacing

  def draw(self, canvas, position):
    canvas.blit(self.character, position)
