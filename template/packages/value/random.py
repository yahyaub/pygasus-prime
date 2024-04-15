import pygame
from pygame.locals import *

import random
import string

class Random:
  @staticmethod
  def number(stop):
    return Random.number_between(1, stop)

  @staticmethod
  def index(stop):
    return Random.number_between(0, stop-1)

  @staticmethod
  def number_between(start, stop):
    random.seed()
    return random.randint(start, stop)

  @staticmethod
  def list_item(list):
    index = Random.index(len(list))
    return list[index]

  @staticmethod
  def alphanumeric(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

  @staticmethod
  def grid_index(x_stop, y_stop):
    x = Random.index(x_stop)
    y = Random.index(y_stop)
    return (x, y)

  @staticmethod
  def grid_item(grid):
    line = Random.list_item(grid)
    return Random.list_item(line)
