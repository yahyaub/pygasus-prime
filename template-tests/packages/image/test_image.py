import pygame

from packages.image.image import Image
from packages.value import variables as vars

def test_can_load_and_retrieve_image():
  Image.load("test_image", "sample.png")

  assert "test_image" in vars.images

  image = Image.get("test_image")
  assert image is vars.images["test_image"]

  assert isinstance(image, pygame.Surface)
  assert image.get_width() > 0
  assert image.get_height() > 0