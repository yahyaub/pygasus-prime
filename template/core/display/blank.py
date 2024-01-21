import pygame
from pygame.locals import *

from packages.display.game import GameDisplay
from packages.display.grid import Grid
from packages.display.layer import Layer, LayerItem, TextItem
from packages.value.constants import BLACK
from packages.value.random import Random

# DISPLAY
class BlankDisplay(GameDisplay):
  def __init__(self, name):
    super().__init__(name, BLACK)

# LAYERS

# ITEMS
