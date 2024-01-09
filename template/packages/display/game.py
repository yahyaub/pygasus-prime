import pygame
from pygame.locals import *

import packages.value.variables as vars

from packages.display.base import BaseDisplay
from packages.value.constants import PURPLE
from packages.value.constants import MAIN_DISPLAY_KEY

class GameDisplay(BaseDisplay):
  def __init__(self, name, bg_colour=False, bg_image=False):
    if not bg_colour:
      bg_colour = PURPLE
    if not bg_image:
      bg_image = pygame.Surface((0,0))

    super().__init__(name, bg_colour, bg_image)

    self.canvas = vars.displays[MAIN_DISPLAY_KEY]
    self.surface = pygame.Surface((self.width, self.height))
    self.layers = []

  def add_layer(self, layer):
    number_of_layers = len(self.layers)

    if number_of_layers < 1:
      layer.set_canvas_to(self)
      self.layers.append(layer)
      return

    if number_of_layers < 10:
      layer.set_canvas_to(self.layers[-1])
      self.layers.append(layer)
      return

  def setup(self):
    for layer in self.layers:
      layer.setup()

  def update(self):
    for layer in self.layers:
      layer.set_dt(self.dt)
      layer.update()

  def update_event(self, event):
    for layer in self.layers:
      layer.update_event(event)

  def draw(self):
    for layer in self.layers:
      layer.clear()
      layer.clear_inactive_items()
      layer.draw()
      self.surface.blit(layer.surface, (0,0))
    self.canvas.surface.blit(self.surface, (0,0))
