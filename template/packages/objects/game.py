import pygame
from pygame.locals import *

import random
import string

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.image.image import Image

class GameObject(ABC):
  def __init__(self, image_key, position, new_dimensions):
    image = Image.get(image_key)
    self.name = image_key + self._get_random_string(4)
    self.image = Image.resize(image, new_dimensions)
    self.position = position
    self.is_active = True
    self.collisions = {}
    self.box = CollisionBox(self)

  def change_name(self, name):
    self.name = name

  def _get_random_string(self, length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def clear(self):
    pass

  @abstractmethod
  def draw(self):
    pass

  @abstractmethod
  def has_collided(self):
    pass
