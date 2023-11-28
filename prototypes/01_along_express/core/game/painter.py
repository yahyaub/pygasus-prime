import pygame
from pygame.locals import *

import packages.value.variables as vars

from packages.value.constants import MAIN_DISPLAY_KEY

class GamePainter:
  def __init__(self):
    self.main_display = vars.displays[MAIN_DISPLAY_KEY]

  def run(self):
    active_display = vars.displays[vars.display_keys[vars.active_display]]

    self.main_display.clear()
    active_display.clear()
    active_display.draw()
    pygame.display.flip()
