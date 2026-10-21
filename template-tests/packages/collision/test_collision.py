import pygame
import pytest

from core.game.starter import GameStarter
from core.game.changer import GameChanger
from core.game.painter import GamePainter

from packages.display.game import GameDisplay
from packages.display.layer import Layer, LayerItem
from packages.image.image import Image
from packages.value import variables as vars
from packages.value.constants import BLACK

@pytest.fixture
def game():

  pygame.init()
  pygame.display.set_mode((1, 1))

  try:
    GameStarter().run()

    changer = GameChanger()
    painter = GamePainter()

    yield changer, painter

  finally:
    pygame.quit()
    vars.displays.clear()
    vars.display_keys.clear()
    vars.active_display = 1
    vars.images.clear()
    vars.text_characters.clear()

@pytest.fixture
def layer():

  class TestLayer(Layer):
      def setup(self):
        pass
      def update(self):
          pass
      def update_self(self):
        pass
      def update_event(self):
        pass
      def draw(self):
        pass

  yield TestLayer()

def test_items_detect_and_clear_collisions(game, layer):
  Image.load("test_image", "sample.png")

  display = GameDisplay("test_display", BLACK)
  display.add_layer(layer)

  item_a = LayerItem("test_image", position=(0, 0))
  item_b = LayerItem("test_image", position=(0, 0))

  item_a.change_name("img_a")
  item_b.change_name("img_b")

  layer.add_item(item_a)
  layer.add_item(item_b)

  display.check_collisions()

  assert item_b.name in item_a.collisions
  assert item_a.name in item_b.collisions

  item_b.position = (10000, 10000)
  item_b.box.adjust(item_b)

  display.check_collisions()

  assert item_b.name not in item_a.collisions
  assert item_a.name not in item_b.collisions