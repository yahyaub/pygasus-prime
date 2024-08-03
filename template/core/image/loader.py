import pygame
from pygame.locals import *

from packages.image.image import Image
from packages.image.spritesheet import ImageSpritesheet

class ImageLoader():
  def run(self):
    images = {
      # key: image_filename
    }

    Image.load_many(images)

class SpritesheetLoader():
  def run(self):
    spritesheets = {
      # key: [image_filename, image_keys]
      "sample": ["sample.png", [["square", "circle"],["triangle", "heart"]]]
    }

    ImageSpritesheet().load_many(spritesheets)
