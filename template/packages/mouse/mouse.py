import pygame
from pygame.locals import *

from packages.display.grid import Grid

class Mouse:
  LEFT_BTN = 1
  MIDDLE_BTN = 2
  RIGHT_BTN = 3
  UP_SCROLL = 4
  DOWN_SCROLL = 5

  @staticmethod
  def get_pos_px():
    return pygame.mouse.get_pos()
  @staticmethod
  def get_x_px():
    return pygame.mouse.get_pos()[0]
  @staticmethod
  def get_y_px():
    return pygame.mouse.get_pos()[1]

  @staticmethod
  def get_pos_num():
    return Grid.tuple_pixel_to_number(Mouse.get_pos())
  @staticmethod
  def get_x_num():
    return Grid.pixel_to_number(Mouse.get_x_px())
  @staticmethod
  def get_y_num():
    return Grid.pixel_to_number(Mouse.get_y_px())

  @staticmethod
  def is_down(event, mouse_button=False):
    if not mouse_button:
      mouse_button = Mouse.LEFT_BTN
    return event.type == MOUSEBUTTONDOWN and event.button == mouse_button
  @staticmethod
  def is_up(event, mouse_button=False):
    if not mouse_button:
      mouse_button = Mouse.LEFT_BTN
    return event.type == MOUSEBUTTONUP and event.button == mouse_button
  @staticmethod
  def is_scroll(event, mouse_button=False):
    return Mouse.is_down(event, mouse_button)

