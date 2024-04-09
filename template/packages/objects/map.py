import pygame
from pygame.locals import *

from abc import abstractmethod
from packages.objects.board import Board
from packages.display.grid import Grid
from packages.display.layer import LayerItem, TextItem

class Map(Board):
  def __init__(self, dimensions, offset, spacing=1):
    super().__init__(dimensions[0], dimensions[1])
    self.legend = {}
    self.off_x = offset[0]
    self.off_y = offset[1]
    self.spacing = spacing

  def setup(self, layer):
    self._set_legends()
    self._set_map()
    self._set_layer(layer)

  def set_legend(self, legend):
    for k, v in legend.legend.items():
      self.legend[k] = v

  def place_defined(self, key_grid):
    keys = Grid.flatten(key_grid)

    index = 0
    row = 0
    col = 0
    row_pos = self.off_x
    col_pos = self.off_y
    while row < self.rows:
      while col < self.cols:

        if index < len(keys):
          row_px = Grid.number_to_pixel(row_pos)
          col_px = Grid.number_to_pixel(col_pos)

          legend = self.legend.get(keys[index])
          if legend == None:
            obj = None
          else:
            obj = MapItem(legend["image_key"], (col_px, row_px), legend["image_type"])
            obj.row = row
            obj.col = col

          self.place(row, col, obj)
          index += 1

        col += 1
        col_pos += self.spacing
      row += 1
      col = 0
      row_pos += self.spacing
      col_pos = self.off_y

  def swap_objs(self, pos_a, pos_b):
    pass
    # item_1 = self.board[pos_a[0]][pos_a[1]]
    # item_2 = self.board[pos_b[0]][pos_b[1]]
    #
    # if (item_1 is None):
    #   self.board[pos_a[0]][pos_a[1]] = item_2
    #   item_2 = None
    #   return
    # if (item_2 is None):
    #   self.board[pos_b[0]][pos_b[1]] = item_1
    #   item_1 = None
    #   return
    #
    # temp = self.board[pos_a[0]][pos_a[1]]
    # self.board[pos_a[0]][pos_a[1]] = self.board[pos_b[0]][pos_b[1]]
    # self.board[pos_b[0]][pos_b[1]] = temp

  def _set_layer(self, layer):
    for row in self.board:
      for col in row:
        if isinstance(col, MapItem):
          layer.add_item(col)

  @abstractmethod
  def _set_legends(self):
    pass
  @abstractmethod
  def _set_map(self):
    pass

class MapItem(LayerItem):
  def __init__(self, image_key, position, image_type):
    super().__init__(image_key, position, image_type)

  def update_event(self, event):
    if event.type == MOUSEBUTTONUP and self.box.is_clicked():
      print(vars(self))

class MapLegend:
  def __init__(self, legend_list):
    self.legend = {}

    for legend in legend_list:
      key = legend[0]
      image_key = legend[1]
      if len(legend) >= 3:
        image_type = legend[2]
        self.update(key, image_key, image_type)
      else:
        self.update(key, image_key)

  def update(self, key, image_key, image_type=False):
    self.legend[key] = {
      "image_key": image_key,
      "image_type": image_type
    }
