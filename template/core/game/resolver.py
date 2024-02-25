import pygame
from pygame.locals import *

import core.value.variables as core_vars
import packages.value.variables as package_vars

class GameResolver:
  def __init__(self):
    pass

  def stop():
    core_vars.game_on = False

  def reset():
    for i in range(1, len(package_vars.displays)):
      display = package_vars.displays[package_vars.display_keys[i]]

      package_vars.displays[package_vars.display_keys[i]] = type(display)(display.name)

      package_vars.displays[package_vars.display_keys[i]].setup()

    package_vars.active_display = 1
