import pygame
from pygame.locals import *

import random

class Random:
  @staticmethod
  def number(start, stop):
    random.seed()
    return random.randint(start, stop)

  @staticmethod
  def list_item(list):
    random.seed()
    index = random.randint(0, len(list)-1)
    return list[index]
