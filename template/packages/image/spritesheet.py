import pygame
from pygame.locals import *

import packages.value.variables as vars

from abc import ABC, abstractmethod
from packages.font.font import Font
from packages.image.image import Image
from packages.objects.text import CharacterObject
from packages.value.constants import DIM, SCALE

class Spritesheet(ABC):
  def load(self, key, filename, keys, points, dim=False):
    if not dim:
      dim = (DIM, DIM)
    dim = (dim[0]*SCALE, dim[1]*SCALE)

    Image.load(key, filename)
    image = Image.get(key)
    resized_image = Image.resize(image, (image.get_width() * SCALE, image.get_height() * SCALE))

    for i in range (0, len(keys)):
      crop_zone = pygame.Surface((dim[0], dim[1]), pygame.SRCALPHA)
      crop_zone.blit(resized_image, (0, 0), (points[i][0] * dim[0], points[i][1] * dim[1], dim[0], dim[1]))
      self.add_image(keys[i], crop_zone)

  def get_keys_and_points(self, image_keys):
    x = 0
    y = 0
    keys = []
    points = []
    for key_list in image_keys:
      for key in key_list:
        keys.append(key)
        points.append((x, y))
        x += 1
      x = 0
      y += 1

    return [keys, points]

  @abstractmethod
  def add_image(self, key, image):
    pass

class ImageSpritesheet(Spritesheet):
  def load_many(self, spritesheets):
    for key, data in spritesheets.items():
      keys_and_points = self.get_keys_and_points(data[1])
      self.load(key, data[0], keys_and_points[0], keys_and_points[1])

  def add_image(self, key, image):
    Image.add(key, image)

class Fontsheet(Spritesheet):
  def __init__(self, dim, spacing):
    horizontal_spacing = (dim[0]*SCALE) + spacing[0]
    vertical_spacing = (dim[1]*SCALE) + spacing[1]

    self.spacing = spacing
    self.spacing_scaled = (horizontal_spacing, vertical_spacing)

  def add_image(self, key, image):
    Font.add_character(key, CharacterObject(image, self.spacing, self.spacing_scaled))
