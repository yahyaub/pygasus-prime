import pygame, pytest
from unittest.mock import patch

import packages.value.variables as vars
from packages.objects.game import GameObject

class DummyGamebject(GameObject):
  def __init__(self, image_key, do_resize=False):
    vars.images[image_key] = pygame.Surface((10, 10))

    if do_resize:
      super().__init__(image_key, "test", (0,0), (1,2))
    else:
      super().__init__(image_key, "test", (0,0))

  def get_image_dim(self):
    return (self.image.get_width(), self.image.get_height())

  def update(self):
    super().update()
  
  def clear(self):
    super().clear()

  def draw(self):
    super().draw()

  def has_collided(self):
    super().has_collided()

class TestGameObject():

  @pytest.fixture(autouse=True)
  def setup_game_obj(self):
    self.game_obj = DummyGamebject("test_image")
    yield
    vars.images = {}

  def test_game_object_is_setup(self):
    assert len(self.game_obj.id) == 14
    assert self.game_obj.type == "test"
    assert self.game_obj.name == "test_image"
    assert self.game_obj.position == (0,0)
    assert self.game_obj.is_active
    assert self.game_obj.is_visible
    assert self.game_obj.collisions == {}
    assert self.game_obj.box.dim == (0,0)
    assert self.game_obj.timer_collection.timers == {}

  def test_game_object_is_resized(self):
    game_obj_resize = DummyGamebject("test_image", True)
    assert game_obj_resize.get_image_dim() == (1,2)

  def test_game_object_can_change_name(self):
    self.game_obj.change_name("quiz")
    assert self.game_obj.name == "quiz"

  def test_game_object_abstract_methods_raise_exceptions(self):
    with pytest.raises(NotImplementedError, match="GameObject.update: Not implemented"):
      self.game_obj.update()

    with pytest.raises(NotImplementedError, match="GameObject.clear: Not implemented"):
      self.game_obj.clear()

    with pytest.raises(NotImplementedError, match="GameObject.draw: Not implemented"):
      self.game_obj.draw()

    with pytest.raises(NotImplementedError, match="GameObject.has_collided: Not implemented"):
      self.game_obj.has_collided()