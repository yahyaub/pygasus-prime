import pygame
from pygame.locals import *

import packages.value.variables as vars

from packages.display.base import BaseDisplay
from packages.image.image import Image
from packages.objects.game import GameObject
from packages.objects.text import TextObject
from packages.value.constants import ORANGE
from packages.value.constants import GRID_DIM
from packages.value.constants import LAYER_DISPLAY_KEY

class Layer(BaseDisplay):
  def __init__(self, canvas, name=False, bg_colour=False, bg_image=False):
    if not name:
      name = LAYER_DISPLAY_KEY
    if not bg_colour:
      bg_colour = pygame.Color(0,0,0,0)
    if not bg_image:
      bg_image = pygame.Surface((0,0))

    super().__init__(name, bg_colour, bg_image)

    self.canvas = canvas
    self.surface = pygame.Surface((self.width, self.height), flags=SRCALPHA)
    self.items = {}
    self.text_items = []

  def add_item(self, item, key=False):
    if not key:
      key = item.name
    self._register_canvas(item)
    self.items[key] = item

  def add_text_item(self, text_item):
    self._register_canvas(text_item)
    self.text_items.append(text_item)

  def draw(self):
    for key, item in self.items.items():
      # pygame.draw.rect(self.surface, ORANGE, item.box.box)
      item.draw()
    for text_item in self.text_items:
      # pygame.draw.rect(self.surface, ORANGE, text_item.box.box)
      text_item.draw()
    self.canvas.surface.blit(self.surface, (0,0))

  def update(self):
    for key, item in self.items.items():
      item.dt = self.dt
      item.update()
    for text_item in self.text_items:
      text_item.dt = self.dt
      text_item.update()
  def update_event(self, event):
    for key, item in self.items.items():
      item.update_event(event)

  def _register_canvas(self, item):
    item.canvas = self.surface

class LayerItem(GameObject):
  def __init__(self, image_key, position=False, new_dimensions=False):
    if not position:
      position = (0,0)
    if not new_dimensions:
      new_dimensions = (GRID_DIM, GRID_DIM)

    super().__init__(image_key, position, new_dimensions)

  def draw(self):
    self.clear()
    self.canvas.blit(self.image, self.position)

  def clear(self):
    self.canvas.fill(0, pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height()))

  def resize(self, new_image_dim, new_collision_dim=False):
    if not new_collision_dim:
      new_collision_dim = (0,0)

    self.image = Image.resize(self.image, new_image_dim)
    self.resize_collision_box(new_collision_dim)

  def change_image(self, image_key):
    self.image = Image.resize(Image.get(image_key), (self.image.get_width(), self.image.get_height()))

class TextItem(TextObject):
  def __init__(self, text, position=False):
    if not position:
      position = (0,0)

    super().__init__(text, position)

  def draw(self):
    self.clear()
    position = self.position
    for ch in self.text:
      # Ideally, this will return the NEXT position for a character
      # eg position = ch.draw(self.canvas, position)
      ch.draw(self.canvas, position)
      position = (position[0] + ch.spacing, position[1])

  def clear(self):
    self.canvas.fill(0, pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height()))
