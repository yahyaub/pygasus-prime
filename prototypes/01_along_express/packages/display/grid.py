import pygame
from pygame.locals import *

from packages.value.constants import GRID_DIM

class Grid:
  @staticmethod
  def snap(pos):
    return (pos[0]*GRID_DIM, pos[1]*GRID_DIM)
