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

  def update_self(self):
    for layer in self.layers:
      layer.update_self()

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

  def check_collisions(self):
    for layer_curr in self.layers:
      for k, item1 in layer_curr.items.items():
        for layer_othr in self.layers:
          for k, item2 in layer_othr.items.items():
            if item1 is item2:
              continue
            if item1.box.has_collided(item2.box):
              item1.collisions[item2.name] = item2
              item2.collisions[item1.name] = item1
            else:
              item1.collisions.pop(item2.name, None)
              item2.collisions.pop(item1.name, None)
