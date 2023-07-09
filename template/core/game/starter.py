import pygame
from pygame.locals import *

# This can be removed for a more appropriate first display
from core.display.blank import BlankDisplay

from core.font.font import MyFont
from core.image.loader import ImageLoader, SpritesheetLoader
from packages.display.main import MainDisplay

class GameStarter:
  def __init__(self):
    pass

  def run(self):
    ImageLoader().run()
    SpritesheetLoader().run()
    MyFont().load()
    self._setup_displays()

  def _setup_displays(self):
    MainDisplay().setup()
    BlankDisplay("blank_display").setup()
