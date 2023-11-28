import pygame
from pygame.locals import *

import packages.value.variables as vars

class Image:
  @staticmethod
  def load(key, filename):
    vars.images[key] = pygame.image.load("assets/images/" + filename)
    return vars.images[key]

  @staticmethod
  def load_many(image_data):
    for key, filename in image_data.items():
      Image.load(key, filename)

  @staticmethod
  def add(key, image):
    vars.images[key] = image

  @staticmethod
  def get(key):
    return vars.images[key]

  @staticmethod
  def resize(image, dimensions):
    return pygame.transform.scale(image, dimensions)

  @staticmethod
  def flip(image, x_flip, y_flip):
    return pygame.transform.flip(image, x_flip, y_flip)
