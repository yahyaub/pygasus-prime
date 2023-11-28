import pygame
from pygame.locals import *

from packages.image.image import Image
from packages.image.spritesheet import ImageSpritesheet

from core.value.constants import SPRITE_KEYS

class ImageLoader():
  def run(self):
    images = {
      # key: image_filename
      "scoreboard": "scoreboard.png"
    }

    Image.load_many(images)

class SpritesheetLoader():
  def run(self):
    spritesheets = {
      # key: [image_filename, image_keys]
      "all": ["sprites_all.png", SPRITE_KEYS]
    }

    ImageSpritesheet().load_many(spritesheets)
