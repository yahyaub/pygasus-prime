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

  while vars.game_on:
    dt = pygame.time.Clock().tick(60.0)
    game_changer.run(dt)
    game_painter.run()
