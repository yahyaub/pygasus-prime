import pygame
from pygame.locals import *

from packages.mouse.mouse import Mouse

class CollisionBox:
  def __init__(self, game_object, dim=False):
    if not dim:
      self.dim = (0, 0)
    self.adjust(game_object)

  def is_clicked(self, offset=False):
    if not offset:
      offset = (0, 0)

    mouse_x = Mouse.get_x_px() - offset[0]
    mouse_y = Mouse.get_y_px() - offset[1]
    mouse_rect = Rect(mouse_x, mouse_y, 1, 1)
    return mouse_rect.colliderect(self.box)

  def has_collided(self, collision_box):
    return self.box.colliderect(collision_box.box)

  def adjust(self, game_object, scale=False):
    if not scale:
      scale = self.dim
    else:
      self.dim = scale

    w = int(game_object.image.get_width() * scale[0])
    h = int(game_object.image.get_height() * scale[1])

    x = game_object.position[0] + w
    y = game_object.position[1] + h

    # Subtracting is the only way that this works properly... I honestly don't know why
    # -ve scale increase the size of the box
    # +ve scale decrease the size of the box
    width = game_object.image.get_width() - (2 * w)
    height = game_object.image.get_height() - (2 * h)
    box = pygame.Rect(x, y, width, height)
    box.topleft = (x, y)

    self.box = box

  def set_dim(self, dim_x, dim_y):
    self.dim = (dim_x, dim_y)

