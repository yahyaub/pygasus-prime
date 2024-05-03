import pygame
from pygame.locals import *

import packages.value.variables as vars

from abc import ABC, abstractmethod
from packages.image.image import Image
from packages.value.constants import BLACK
from packages.value.constants import MAIN_DISPLAY_KEY, MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT
from packages.value.constants import LAYER_DISPLAY_KEY

class Display():
  @staticmethod
  def switch(key, reset=True):
    if not key == MAIN_DISPLAY_KEY:
      if reset:
        vars.displays[key].reset()
      vars.active_display = vars.display_keys.index(key)

class BaseDisplay(ABC):
  def __init__(self, name, bg_colour, bg_image):
    self.width = MAIN_DISPLAY_WIDTH
    self.height = MAIN_DISPLAY_HEIGHT
    self.bg_colour = bg_colour

    self.bg_image = bg_image
    if bg_image.get_width() > 0 or bg_image.get_height() > 0:
      self.bg_image = Image.resize(bg_image, (self.width, self.height))

    if not name == LAYER_DISPLAY_KEY:
      self.name = name
      vars.displays[name] = self
      vars.display_keys.append(name)

  def clear(self):
    self.surface.fill(self.bg_colour)
    self.surface.blit(self.bg_image, (0,0))

  def set_dt(self, dt):
    self.dt = dt

  @abstractmethod
  def setup(self):
    pass

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def update_self(self):
    pass

  @abstractmethod
  def update_event(self):
    pass

  @abstractmethod
  def draw(self):
    pass
