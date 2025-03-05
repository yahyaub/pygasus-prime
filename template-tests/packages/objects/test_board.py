import pytest

from packages.objects.board import Board, SimpleBoard

class DummyBoard(Board):
  def __init__(self):
    super().__init__(1, 2)

  def get_spaces(self):
    return (self.board[0][0], self.board[0][1])
  
  def place_defined(self, obj_grid):
    return super().place_defined(obj_grid)

  def swap_objs(self, pos_a, pos_b):
    return super().swap_objs(pos_a, pos_b)

class TestBoard():

  @pytest.fixture(autouse=True)
  def setup_board(self):
    self.board = DummyBoard()

  def test_initial_board_empty(self):
    spaces = self.board.get_spaces()
    assert spaces[0] == None and spaces[1] == None

  def test_board_placement(self):
    self.board.place(0,1, 1)
    spaces = self.board.get_spaces()
    assert spaces[0] == None and spaces[1] == 1

  def test_board_cannot_repeat_placement(self):
    self.board.place(0,1, 1)
    self.board.place(0,1, 2)
    spaces = self.board.get_spaces()
    assert spaces[0] == None and spaces[1] == 1

  def test_board_random_placement(self):
    self.board.place_random(1)
    spaces = self.board.get_spaces()
    assert spaces[0] == 1 or spaces[1] == 1

  def test_board_failed_repeat_random_placement(self):
    is_success = True
    for _ in range (0,10):
      is_success = is_success and self.board.place_random(1)
    assert is_success == False

  # Update the test to stress this function
  # Maybe on a 100x100 grid?
  def test_board_random_placement_beta(self):
    self.board.place_random_beta(1)
    self.board.place_random_beta(2)
    spaces = self.board.get_spaces()
    assert (spaces[0] == 1 or spaces[1] == 1) and (spaces[0] == 2 or spaces[1] == 2)

  def test_board_failed_repeat_random_placement_beta(self):
    is_success = True
    for _ in range (0,10):
      is_success = is_success and self.board.place_random_beta(1)
    assert is_success == False

  def test_board_abstract_methods_raise_exceptions(self):
    with pytest.raises(NotImplementedError, match="Board.place_defined: Not implemented"):
      self.board.place_defined([[]])

    with pytest.raises(NotImplementedError, match="Board.swap_objs: Not implemented"):
      self.board.swap_objs(0, 0)

class DummySimpleBoard(SimpleBoard):
  def __init__(self):
    super().__init__(1, 2)

  def get_spaces(self):
    return (self.board[0][0], self.board[0][1])

class TestSimpleBoard():

  @pytest.fixture(autouse=True)
  def setup_board(self):
    self.board = DummySimpleBoard()

  def test_board_placement_defined(self):
    self.board.place_defined([[1,2]])
    spaces = self.board.get_spaces()
    assert spaces[0] == 1 and spaces[1] == 2

  def test_board_swap_objects(self):
    self.board.place_defined([[1,2]])
    self.board.swap_objs((0,0), (0,1))
    spaces = self.board.get_spaces()
    assert spaces[0] == 2 and spaces[1] == 1