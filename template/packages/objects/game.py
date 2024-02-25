import pygame
from pygame.locals import *

from abc import ABC, abstractmethod
from packages.collision.collision import CollisionBox
from packages.image.image import Image
from packages.time.timer import TimerCollection
from packages.value.random import Random

class GameObject(ABC):
  def __init__(self, image_key, image_type, position, new_dimensions):
    image = Image.get(image_key)
    self.id = image_key + Random.alphanumeric(4)
    self.type = image_type
    self.name = image_key
    self.image = Image.resize(image, new_dimensions)
    self.position = position
    self.is_active = True
    self.is_visible = True
    self.collisions = {}
    self.box = CollisionBox(self)
    self.timers = TimerCollection()

  def change_name(self, name):
    self.name = name

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
