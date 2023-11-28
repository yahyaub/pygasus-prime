import pygame
from pygame.locals import *

import sys
import packages.value.variables as vars

class GameChanger:
  def run(self, dt):
    active_display = vars.displays[vars.display_keys[vars.active_display]]

    active_display.set_dt(dt)
    active_display.update()

    for event in pygame.event.get():
      if event.type == QUIT:
        self.quit_game()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          self.quit_game()

      active_display.update_event(event)

  def quit_game(self):
    pygame.quit()
    sys.exit()
