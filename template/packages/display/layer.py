import pygame
from pygame.locals import *

import packages.value.variables as vars

from packages.display.base import BaseDisplay
from packages.display.grid import Grid
from packages.image.image import Image
from packages.objects.game import GameObject
from packages.objects.text import TextObject
from packages.value.constants import BLUE
from packages.value.constants import GRID_DIM
from packages.value.constants import LAYER_DISPLAY_KEY

class Layer(BaseDisplay):
  def __init__(self, name=False, bg_colour=False, bg_image=False):
    if not name:
      name = LAYER_DISPLAY_KEY
    if not bg_colour:
      bg_colour = pygame.Color(0,0,0,0)
    if not bg_image:
      bg_image = pygame.Surface((0,0))

    super().__init__(name, bg_colour, bg_image)

    self.surface = pygame.Surface((self.width, self.height), flags=SRCALPHA)
    self.items = {}
    self.text_items = []

  def add_item(self, item, key=False):
    if item is None:
      return
    if not key:
      key = item.id
    self._set_as_layer_for(item)
    self.items[key] = item

  def remove_item(self, key=False):
    if not key:
      key = item.id
    del self.items[key]

  def add_text_item(self, text_item):
    if text_item is None:
      return
    self._set_as_layer_for(text_item)
    self.text_items.append(text_item)

  def draw(self):
    for key, item in self.items.items():
      item.box.adjust(item)
      # pygame.draw.rect(self.surface, BLUE, item.box.box)
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

  def clear_inactive_items(self):
    self.items = dict(list(filter((lambda itm: itm[1].is_active), self.items.items())))

  def set_canvas_to(self, canvas):
    self.canvas = canvas

  def update_self(self):
    pass

  def _set_as_layer_for(self, item):
    item.canvas = self.surface
    item.layer = self

class LayerItem(GameObject):
  def __init__(self, image_key, position=False, image_type=False, new_dimensions=False):
    if not image_type:
      image_type = image_key
    if not position:
      position = (0,0)
    if not new_dimensions:
      new_dimensions = (GRID_DIM, GRID_DIM)

    x_px = Grid.number_to_pixel(position[0])
    y_px = Grid.number_to_pixel(position[1])
    px_position = (x_px, y_px)

    super().__init__(image_key, image_type, px_position, new_dimensions)

  def update(self):
    pass

  def update_event(self, event):
    pass

  def draw(self):
    if self.is_visible:
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

  def has_collided(self):
    return len(self.collisions)> 0

class FreeLayerItem(LayerItem):
  def __init__(self, image_key, position=False, image_type=False, new_dimensions=False):
    if not image_type:
      image_type = image_key
    if not position:
      position = (0,0)
    if not new_dimensions:
      new_dimensions = (GRID_DIM, GRID_DIM)

    super().__init__(image_key, position, image_type, new_dimensions)
    self.position = position

class TextItem(TextObject):
  def __init__(self, text, position=False):
    if not position:
      position = (0,0)

    super().__init__(text, position)

  def update(self):
    pass

  def update_event(self, event):
    pass

  def draw(self):
    self.clear()
    position = self.position
    for ch in self.text:
      position = ch.draw(self.canvas, position)

  def clear(self):
    self.canvas.fill(0, pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height()))
