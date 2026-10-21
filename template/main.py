import pygame
from pygame.locals import *

import core.value.variables as vars

from core.game.starter import GameStarter
from core.game.changer import GameChanger
from core.game.painter import GamePainter

if __name__ == '__main__':
  pygame.init()
  GameStarter().run()

  game_changer = GameChanger()
  game_painter = GamePainter()

  clock = pygame.time.Clock()
  while vars.game_on:
    dt = clock.tick(90.0)
    game_changer.run(dt)
    game_painter.run()
  game_changer.quit_game()
