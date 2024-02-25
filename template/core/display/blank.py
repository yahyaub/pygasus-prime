import pygame
from pygame.locals import *

# Global variables
import core.value.variables as core_vars

from packages.display.game import GameDisplay
from packages.display.grid import Grid
from packages.display.layer import Layer, LayerItem, TextItem
from packages.value.constants import BLACK
from packages.value.random import Random

# VARS (scoped to this display adn its layers)
class GameVars():
  is_game_over = False

# DISPLAY
class BlankDisplay(GameDisplay):
  def __init__(self, name):
    super().__init__(name, BLACK)

    self.add_layer(BlankLayer)

# LAYERS
class BlankLayer(Layer):
  def __init__(self):
    super().__init__()

  def setup(self):
    # self.add_item(SampleItem("sample", 0, 0))
    pass

# ITEMS
'''
class SampleItem(LayerItem):
  def __init__(self, image_key, x, y):
    super().__init__(image_key, (x, y))
'''
