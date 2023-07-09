import pygame
from pygame.locals import *

from packages.display.game import GameDisplay
from packages.value.constants import BLACK

# DISPLAY
class BlankDisplay(GameDisplay):
  def __init__(self, name):
    super().__init__(name, BLACK)

# LAYERS

# ITEMS
