import pygame
from pygame.locals import *

from packages.value.constants import GRID_DIM

class Grid:
  @staticmethod
  def number_to_pixel(number):
    return number*GRID_DIM

  @staticmethod
  def pixel_to_number(pixel):
    return pixel // GRID_DIM

  @staticmethod
  def list_number_to_pixel(number_list):
    pixel_list = []
    for number in number_list:
      pixel_list.append(Grid.number_to_pixel(number))

    return pixel_list

  @staticmethod
  def list_pixel_to_number(pixel_list):
    number_list = []
    for pixel in pixel_list:
      number_list.append(Grid.pixel_to_number(pixel))

    return number_list

  @staticmethod
  def tuple_number_to_pixel(number_tuple):
    return tuple(Grid.list_number_to_pixel(list(number_tuple)))

  @staticmethod
  def tuple_pixel_to_number(pixel_tuple):
    return tuple(Grid.list_pixel_to_number(list(pixel_tuple)))

  @staticmethod
  def flatten(grid):
    flat_list = []

    for row in grid:
      flat_list.extend(row)

    return flat_list
