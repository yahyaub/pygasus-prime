import pygame
from pygame.locals import *

from abc import ABC, abstractmethod
from packages.value.random import Random
from packages.display.grid import Grid

class Board(ABC):
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.board = [[None for _ in range(cols)] for _ in range(rows)]
    self.space_count = rows * cols

  def place(self, row, col, obj):
    if self._is_empty(row, col):
      self.board[row][col] = obj
      return True
    return False

  # This 100% does not guarantee that an obj is placed.
  def place_random(self, obj):
    index = Random.grid_index(self.rows, self.cols)
    return self.place(index[0], index[1], obj)

  # There is a better chance for an obj to be placed.
  # The try limit aims to combat randomness and infinite loops.
  def place_random_beta(self, obj):
    is_placed = self.place_random(obj)
    try_limit = self.rows * self.cols
    while (not is_placed) and (try_limit > 0):
      is_placed = self.place_random(obj)
      try_limit -= 1

    if is_placed:
      return True
    return False

  def link_board(self):
    pass

  # When passing 1D lists, remember to wrap them in a [ ]
  # e.g. like this -> [ [1,2,3,4,5,6,7] ]
  @abstractmethod
  def place_defined(self, obj_grid):
    pass

  @abstractmethod
  def swap_objs(self, pos_a, pos_b):
    pass

  def _is_empty(self, row, col):
    return self.board[row][col] == None

class DataBoard(Board):
  def __init__(self, rows, cols):
    super().__init__(rows, cols)

  def place_defined(self, obj_grid):
    objs = Grid.flatten(obj_grid)

    row = 0
    col = 0
    index = 0
    while row < self.rows:
      while col < self.cols:

        if index < len(objs):
          self.place(row, col, objs[index])
          index += 1

        col += 1
      row += 1
      col = 0

  def swap_objs(self, pos_a, pos_b):
    temp = self.board[pos_a[0]][pos_a[1]]
    self.board[pos_a[0]][pos_a[1]] = self.board[pos_b[0]][pos_b[1]]
    self.board[pos_b[0]][pos_b[1]] = temp
