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
    return Random.number_between(0, stop)

  @staticmethod
  def number_between(start, stop):
    random.seed()
    return random.randint(start, stop)

  @staticmethod
  def list_item(list):
    random.seed()
    index = random.randint(0, len(list)-1)
    return list[index]

  @staticmethod
  def alphanumeric(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))
