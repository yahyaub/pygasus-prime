import pygame
import pytest

from core.game.starter import GameStarter
from core.game.changer import GameChanger
from core.game.painter import GamePainter

from packages.display.base import Display
from packages.display.game import GameDisplay
from packages.display.layer import Layer, LayerItem
from packages.image.image import Image
from packages.value import variables as vars
from packages.value.constants import MAIN_DISPLAY_KEY, BLACK


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


def test_core_starts_and_renders_one_frame(game):
  changer, painter = game

  assert MAIN_DISPLAY_KEY in vars.displays

  changer.run(16)
  painter.run()

  assert pygame.display.get_init()

def test_can_switch_active_display(game):
  assert "blank_display" in vars.displays

  Display.switch("blank_display")

  expected_index = vars.display_keys.index("blank_display")
  assert vars.active_display == expected_index

  changer, painter = game
  changer.run(16)
  painter.run()

def test_can_load_and_retrieve_image(game):
  Image.load("test_image", "sample.png")

  assert "test_image" in vars.images

  image = Image.get("test_image")
  assert image is vars.images["test_image"]

  assert isinstance(image, pygame.Surface)
  assert image.get_width() > 0
  assert image.get_height() > 0

def test_image_transformations(game):
  Image.load("test_image", "sample.png")

  original = Image.get("test_image")

  resized = Image.resize(original, (120, 240))
  assert resized.get_size() == (120, 240)

  flipped = Image.flip(original, True, False)
  assert isinstance(flipped, pygame.Surface)
  assert flipped.get_size() == original.get_size()

def test_image_transformations_preserve_original(game):
  Image.load("test_image", "sample.png")

  original = Image.get("test_image")
  original_size = original.get_size()

  resized = Image.resize(original, (120, 240))
  flipped = Image.flip(original, True, False)

  assert original.get_size() == original_size
  assert resized.get_size() == (120, 240)
  assert flipped.get_size() == original_size
  assert resized is not original
  assert flipped is not original

def test_items_detect_and_clear_collisions(game):
  Image.load("test_image", "sample.png")

  display = GameDisplay("test_display", BLACK)

  class TestLayer(Layer):
    def setup(self):
      pass

  layer = TestLayer()
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

def test_keyboard_event_reaches_active_layer(game):
  class TestLayer(Layer):
    def __init__(self):
      super().__init__("test")

      self.received_events = []

    def setup(self):
      pass

    def update_event(self, event):
      self.received_events.append(event)

  display = GameDisplay("test_display", BLACK)
  layer = TestLayer()
  display.add_layer(layer)
  display.setup()

  Display.switch("test_display")

  event = pygame.event.Event(
      pygame.KEYDOWN,
      key=pygame.K_SPACE,
      unicode=" "
  )
  pygame.event.post(event)

  changer, painter = game
  changer.run(16)

  assert any(
      received.type == pygame.KEYDOWN
      and received.key == pygame.K_SPACE
      for received in layer.received_events
  )

def test_keyboard_event_reaches_item(game):
  class TestItem:
    def __init__(self):
      self.id = "test_item"
      self.is_active = True
      self.received_events = []

    def update_event(self, event):
      self.received_events.append(event)

    def update(self):
      pass

  class TestLayer(Layer):
    def __init__(self):
      super().__init__("test_layer")

    def setup(self):
      pass

  display = GameDisplay("test_display", BLACK)
  layer = TestLayer()
  item = TestItem()

  display.add_layer(layer)
  display.setup()
  Display.switch("test_display", reset=False)
  layer.add_item(item)

  event = pygame.event.Event(
    pygame.KEYDOWN,
    key=pygame.K_SPACE,
    unicode=" "
  )
  pygame.event.post(event)

  changer, painter = game
  changer.run(16)

  assert any(
    received.type == pygame.KEYDOWN
    and received.key == pygame.K_SPACE
    for received in item.received_events
  )

def test_display_switch_reset_behaviour(game):
  class TestLayer(Layer):
      def __init__(self):
          super().__init__("test_layer")
          self.setup_count = 0

      def setup(self):
          self.setup_count += 1
          self.items["setup_item"] = {}

  display = GameDisplay("test_display", BLACK)
  layer = TestLayer()
  display.add_layer(layer)
  display.setup()

  assert layer.setup_count == 1
  assert "setup_item" in layer.items

  layer.items["extra_item"] = {}
  Display.switch("test_display", reset=False)

  assert "extra_item" in layer.items
  assert layer.setup_count == 1

  layer.items["extra_item"] = object()
  Display.switch("test_display", reset=True)

  assert "extra_item" not in layer.items
  assert "setup_item" in layer.items
  assert layer.setup_count == 2

def test_inactive_items_are_removed(game):
  class TestLayer(Layer):
      def __init__(self):
          super().__init__("test_layer")

      def setup(self):
          pass

  class TestItem:
    def __init__(self, item_id, is_active):
        self.id = item_id
        self.is_active = is_active

  layer = TestLayer()

  active_item = TestItem("active", True)
  inactive_item = TestItem("inactive", False)

  layer.add_item(active_item)
  layer.add_item(inactive_item)

  layer.clear_inactive_items()

  assert "active" in layer.items
  assert "inactive" not in layer.items

def test_delta_time_reaches_active_layer_and_item(game):
  class TestItem:
    def __init__(self):
      self.id = "item"
      self.is_active = True
      self.received_dt = None

    def update(self):
      self.received_dt = self.dt

    def update_event(self, event):
      pass

  class TestLayer(Layer):
    def __init__(self):
      super().__init__("test_layer")
      self.received_dt = None

    def setup(self):
      pass

    def update(self):
      self.received_dt = self.dt
      super().update()

  display = GameDisplay("test_display", BLACK)
  layer = TestLayer()
  item = TestItem()

  display.add_layer(layer)
  layer.add_item(item)
  display.setup()

  Display.switch("test_display", reset=False)

  changer, painter = game
  changer.run(37)

  assert display.dt == 37
  assert layer.received_dt == 37
  assert item.received_dt == 37

def test_all_items_receive_delta_time(game):
  Image.load("test_image", "sample.png")

  class TestItem(LayerItem):
    def __init__(self, item_id):
      super().__init__("test_image", position=(0,0))
      self.id = item_id
      self.is_active = True
      self.received_dt = None
      self.update_count = 0

    def update(self):
      self.received_dt = self.dt
      self.update_count += 1

    def update_event(self, event):
      pass

  class TestLayer(Layer):
    def __init__(self):
      super().__init__("test_layer")

    def setup(self):
      pass

  display = GameDisplay("test_display", BLACK)
  layer = TestLayer()

  item_a = TestItem("item_a")
  item_b = TestItem("item_b")

  display.add_layer(layer)
  display.setup()
  Display.switch("test_display", reset=False)

  layer.add_item(item_a)
  layer.add_item(item_b)

  changer, painter = game
  changer.run(37)

  assert item_a.received_dt == 37
  assert item_b.received_dt == 37
  assert item_a.update_count == 1
  assert item_b.update_count == 1