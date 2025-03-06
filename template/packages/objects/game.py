import pygame
from pygame.locals import *

from abc import ABC, abstractmethod
from typing import Any, Optional
from packages.collision.collision import CollisionBox
from packages.image.image import Image
from packages.time.timer import TimerCollection
from packages.value.random import Random

class GameObject(ABC):
  def __init__(self, image_key:str, image_type:str, position:tuple[int,int], new_dimensions:Optional[tuple[int, int]]=None):
    image = Image.get(image_key)

    if new_dimensions == None:
      new_dimensions = (image.get_width(), image.get_height())

    self.id = image_key + Random.alphanumeric(4)
    self.type = image_type
    self.name = image_key
    self.image = Image.resize(image, new_dimensions)
    self.position = position
    self.is_active = True
    self.is_visible = True
    self.collisions = {}

    # TODO: Initial value of this should be image dimension
    self.box = CollisionBox(self)
    self.timer_collection = TimerCollection()

  def change_name(self, name:str):
    self.name = name

  @abstractmethod
  def update(self):
    raise NotImplementedError("GameObject.update: Not implemented")

  @abstractmethod
  def clear(self):
    raise NotImplementedError("GameObject.clear: Not implemented")

  @abstractmethod
  def draw(self):
    raise NotImplementedError("GameObject.draw: Not implemented")

  @abstractmethod
  def has_collided(self):
    raise NotImplementedError("GameObject.has_collided: Not implemented")
