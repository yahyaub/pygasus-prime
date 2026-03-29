import pygame, pytest

import packages.value.variables as vars
from packages.objects.map import Map, MapItem, MapLegend
from packages.display.layer import Layer

@pytest.fixture(autouse=True)
def mock_grid(monkeypatch):
  monkeypatch.setattr("packages.objects.map.Grid.flatten", lambda x: sum(x, []))
  monkeypatch.setattr("packages.objects.map.Grid.number_to_pixel", lambda x: x * 10)

class MockMap(Map):
  def __init__(self, dimensions, offset):
    super().__init__(dimensions, offset)
    vars.images = {
      "img_a": pygame.Surface((1, 1)),
      "img_b": pygame.Surface((1, 1))
    }
               
  def _set_legends(self):
    pass

  def _set_map(self):
    pass

class MockLayer(Layer):
  def setup(self):
    pass

  def update(self):
    pass

  def update_self(self):
    pass

  def update_event(self):
    pass

  def draw(self):
    pass

class TestMapLegend():
  def test_map_legend_setup_with_type(self):
    map_legend = MapLegend([
      ["key", "image_key", "image_type"]
    ])

    map_legend_data = map_legend.legend["key"]

    has_image_key = map_legend_data["image_key"] == "image_key"
    has_image_type = map_legend_data["image_type"] == "image_type"
    assert has_image_key and has_image_type

  def test_map_legend_setup_with_no_type(self):
    map_legend = MapLegend([
      ["key", "image_key"]
    ])

    map_legend_data = map_legend.legend["key"]

    has_image_key = map_legend_data["image_key"] == "image_key"
    has_image_type = map_legend_data["image_type"] == None
    assert has_image_key and has_image_type

class TestMap():
  def test_place_defined(self):
    mock_map = MockMap((2, 2), (0, 0))

    legend = MapLegend([
      ["A", "img_a"],
      ["B", "img_b"]
    ])
    mock_map.set_legend(legend)

    grid = [
      ["A", "B"],
      ["B", "A"]
    ]

    mock_map.place_defined(grid)
    vars.images = {}

    for r in range(2):
      for c in range(2):
        item = mock_map.board[r][c]
        assert isinstance(item, MapItem)
        assert item.row == r
        assert item.col == c


  def test_place_defined_with_unknown_key(self):
    mock_map = MockMap((1, 1), (0, 0))
    mock_map.set_legend(MapLegend([["A", "img_a"]]))

    grid = [["X"]]

    mock_map.place_defined(grid)
    vars.images = {}

    assert mock_map.board[0][0] is None

  def test_place_defined_with_partial_grid(self):
    mock_map = MockMap((2, 2), (0, 0))
    mock_map.set_legend(MapLegend([["A", "img_a"]]))

    grid = [["A"]]

    mock_map.place_defined(grid)
    vars.images = {}

    assert mock_map.board[0][0] is not None
    assert mock_map.board[0][1] is None
    assert mock_map.board[1][0] is None
    assert mock_map.board[1][1] is None

  def test_set_legend_combines_legends(self):
    mock_map = MockMap((1,1), (0,0))

    l1 = MapLegend([["A", "img_a"]])
    l2 = MapLegend([["B", "img_b"]])

    mock_map.set_legend(l1)
    mock_map.set_legend(l2)
    vars.images = {}

    assert "A" in mock_map.legend
    assert "B" in mock_map.legend

  def test_map_layer_integration(self):
    mock_map = MockMap((1,1), (0,0))
    layer = MockLayer()

    mock_map.board = [[MapItem("img_a", (0,0), None)]]

    mock_map._set_layer(layer)
    vars.images = {}

    assert len(layer.items) == 1

  