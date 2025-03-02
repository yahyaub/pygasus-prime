from packages.value import variables

def test_initial_display_dict_is_empty():
  assert variables.displays == {}

def test_initial_display_keys_list_is_empty():
  assert variables.display_keys == []

def test_initial_active_display_is_the_first():
  assert variables.active_display == 1

def test_initial_images_dict_is_empty():
  assert variables.images == {}

def test_initial_text_character_mapping_dict_is_empty():
  assert variables.text_characters == {}