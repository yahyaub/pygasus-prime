from packages.value import constants

def test_default_grid_dimension_is_16px():
  assert constants.DIM == 16

def test_default_grid_scale_is_4px():
  assert constants.SCALE == 4

def test_default_main_display_key():
  assert constants.MAIN_DISPLAY_KEY == "main"

def test_default_layer_display_key():
  assert constants.LAYER_DISPLAY_KEY == "_layer"

def test_colour_black_present():
  assert constants.BLACK == (0, 0, 0)

def test_colour_white_present():
  assert constants.WHITE == (255, 255, 255)

def test_colour_green_present():
  assert constants.GREEN == (128, 255, 0)