import re

from packages.value.random import Random

def test_random_number():
  random_number = Random.number(2)
  assert random_number == 1 or random_number == 2

def test_random_number_between():
  random_number = Random.number_between(0,1)
  assert random_number == 0 or random_number == 1

def test_random_alphanumeric():
  assert bool(re.fullmatch(r'[A-Za-z0-9]+', Random.alphanumeric(8)))

def test_random_list_item():
  list_item = Random.list_item([1,2])
  assert list_item == 1 or list_item == 2

def test_random_grid_item():
  grid_item = Random.grid_item([[1],[2]])
  assert grid_item == 1 or grid_item == 2

def test_random_grid_index():
  grid_index = Random.grid_index(2,1)
  assert grid_index == (0,0) or grid_index == (1,0)