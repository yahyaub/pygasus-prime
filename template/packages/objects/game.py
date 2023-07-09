import pygame
from pygame.locals import *

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.image.image import Image

class GameObject(ABC):
  def __init__(self, image_key, position, new_dimensions):
    image = Image.get(image_key)
    self.name = image_key
    self.image = Image.resize(image, new_dimensions)
    self.position = position
    self.is_active = True
    self.box = CollisionBox(self)

  def resize_collision_box(self, scale):
    self.box = CollisionBox(self, scale)

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def clear(self):
    pass

  @abstractmethod
  def draw(self):
    pass
