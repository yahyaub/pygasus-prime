import pygame
from pygame.locals import *

from packages.display.base import BaseDisplay
from packages.value.constants import PURPLE
from packages.value.constants import MAIN_DISPLAY_KEY

class MainDisplay(BaseDisplay):
  def __init__(self):
    bg_colour = PURPLE
    bg_image = pygame.Surface((0,0))
    super().__init__(MAIN_DISPLAY_KEY, bg_colour, bg_image)

    self.surface = pygame.display.set_mode((self.width, self.height))

  def setup(self):
    pass

  def update(self):
    pass

  def update_event(self, event):
    pass

  def update_self(self):
    pass

  def draw(self):
    pass
