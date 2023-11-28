import random
import pygame
from pygame.locals import *

from packages.display.game import GameDisplay
from core.value.constants import ORANGE

from packages.display.grid import Grid
from packages.display.layer import Layer, LayerItem, TextItem

# TODO add a random package for this stuff
def get_random_number(start, stop):
  random.seed()
  return random.randint(start, stop)

def get_random_list_item(lst):
  random.seed()
  index = random.randint(0, len(lst)-1)
  return lst[index]

# DISPLAY
class BlankDisplay(GameDisplay):
  def __init__(self, name):
    super().__init__(name, ORANGE)

    # TODO Ensure layering is done automatically when calling add_layer
    road_layer = RoadLayer(self)
    car_layer = CarLayer(road_layer)

    self.add_layer(road_layer)
    self.add_layer(car_layer)


# LAYERS
class RoadLayer(Layer):
  def __init__(self, canvas):
    super().__init__(canvas)

  def setup(self):
    x = 0
    y = 0
    label = 1
    while x < 6:
      while y < 9:
        road = Road(x, y)
        self.add_item(road, road.name+str(label))
        y += 1
        label += 1
      x += 1
      y = 0

    self.scoreboard = PlayerScoreBoard(3, 0)
    self.scoreboard.resize(Grid.snap((4,1)))
    self.add_item(self.scoreboard)

class CarLayer(Layer):
  def __init__(self, canvas):
    super().__init__(self, canvas)

    self.count = 1
    self.max_cars = 10

    self.stopwatch = {
      "last_ticks": 0,
      "now_ticks": 0,
      "seconds": 0,
      "reset_seconds": 2
    }
    self.stopwatch["seconds"] = self.stopwatch["reset_seconds"]

  def setup(self):
    offset_x = 2
    offset_y = -1.3

    self.player_car = PlayerCar(2 + offset_x, 5 + offset_y)
    self.add_item(self.player_car)

    self.lives = [0]*self.player_car.lives
    y = 1
    for i in range(0,len(self.lives)):
      self.lives[i] = PlayerLife(0.5, y)
      self.add_item(self.lives[i], "player_life_"+str(i))
      y += 1.2

    self.score = PlayerScore(3.2, 0)
    self.add_text_item(self.score)

  def spawn_passenger(self):
    offset_x = 2
    offset_y = -1.3

    passenger = Passenger(0 + offset_x, 0 + offset_y)
    self.add_item(passenger)

  def spawn_car(self):
    offset_x = 2
    offset_y = -1.3

    car_key = 'car_'+str(self.count)
    car_x = get_random_list_item([1,2,3,4])
    car_y = 8.7
    car_speed = get_random_number(1,5)
    car = CarUp(car_x + offset_x, car_y + offset_y, car_speed)

    for k, c in self.items.items():
      if car.box.has_collided(c.box):
        return

    self.item_buffer.append([car_key, car])
    self.count += 1

  def update_self(self):
    total = 0
    passenger_there = False
    items = self.items.items()
    for key, value in items:
      if "car_" in key:
        total += 1
      if "passenger" == key or self.player_car.passenger or self.player_car.dropped_passenger:
        passenger_there = True

    if not passenger_there:
      self.spawn_passenger()
    if self.player_car.dropped_passenger:
      self.add_item(Passenger(5 + 2, (self.player_car.position[1]/64) + 0.3))
      self.player_car.dropped_passenger = False

    if total < self.max_cars and self.stopwatch["seconds"] >= self.stopwatch["reset_seconds"]:
      self.spawn_car()
      self.stopwatch["last_ticks"] = 0
      self.stopwatch["now_ticks"] = 0
      self.stopwatch["seconds"] = 0

    if self.player_car.lives < len(self.lives) > 0:
      life = self.lives.pop(-1)
      life.is_active = False

    if pygame.time.get_ticks() - self.stopwatch["now_ticks"] >= 1000:
      self.stopwatch["last_ticks"] = self.stopwatch["now_ticks"]
      self.stopwatch["now_ticks"] = pygame.time.get_ticks()
      self.stopwatch["seconds"] += 1

    self.score.set_text(str(int(self.player_car.score["value"]/1000)))


# ITEMS
class Road(LayerItem):
  def __init__(self, x, y):
    offset_x = 2
    offset_y = -1.3

    x = x + offset_x
    y = y + offset_y
    super().__init__("road", Grid.snap((x,y)))

  def update(self):
    pass

  def update_event(self, event):
    pass

class PlayerLife(LayerItem):
  def __init__(self, x, y):
    super().__init__("player", Grid.snap((x,y)))

  def update(self):
    pass

  def update_event(self, event):
    pass

class PlayerScoreBoard(LayerItem):
  def __init__(self, x, y):
    super().__init__("scoreboard", Grid.snap((x,y)))

  def update(self):
    pass

  def update_event(self, event):
    pass

class PlayerScore(TextItem):
  def __init__(self, x, y):
    super().__init__("0", Grid.snap((x,y)))

  def update(self):
    pass

  def update_event(self, event):
    pass

class PlayerCar(LayerItem):
  def __init__(self, x, y):
    super().__init__("player", Grid.snap((x,y)))

    self.collision_dim = (0.15, 0)
    self.horizontal_speed = 6
    self.vertical_speed = 3
    self.moving = {
      "left": [False, -1],
      "right": [False, 1],
      "up": [False, -2],
      "down": [False, 2]
    }
    self.lives = 3
    self.passenger = False
    self.dropped_passenger = False
    self.passenger_count = 0

    self.score = {
      "value": 0,
      "increment": 1,
      "multiplier": 1,
      "multiplier_increment": 0
    }

  def update(self):
    for k, c in self.layer.items.items():
      if (not self is c) and self.box.has_collided(c.box) and "car_" in k:
        self.lives -= 1
        self.passenger = False
        if self.lives < 1:
          self.is_active = False
      else:
        if (Grid.snap((7,0))[0] - 20) > self.position[0] > (Grid.snap((2,0))[0] + 20):
          self.score["value"] += self.score["increment"] * (self.score["multiplier"] + self.score["multiplier_increment"])

    self._move("up")
    self._move("down")
    self._move("left")
    self._move("right")

    if self.position[0] >= Grid.snap((7,0))[0] and self.passenger:
      self.passenger = False
      self.dropped_passenger = True
      self.passenger_count += 1
      self.score["increment"] += 0.05
      self.score["multiplier_increment"] += 2

      if self.passenger_count % 1 == 0:
        self.score["multiplier"] *= 1.35

  def update_event(self, event):
    if event.type == KEYDOWN:
      if event.key == K_w:
        self._start_movement("up")
      if event.key == K_s:
        self._start_movement("down")
      if event.key == K_a:
        self._start_movement("left")
      if event.key == K_d:
        self._start_movement("right")
    if event.type == KEYUP:
      if event.key == K_w:
        self._stop_movement("up")
      if event.key == K_s:
        self._stop_movement("down")
      if event.key == K_a:
        self._stop_movement("left")
      if event.key == K_d:
        self._stop_movement("right")

  def _move(self, direction):
    pos_x = self.position[0]
    pos_y = self.position[1]

    is_moving = self.moving[direction][0]
    dir_value = self.moving[direction][1]

    new_x = pos_x
    new_y = pos_y
    if is_moving and dir_value % 2 == 0:
      new_y += (self.vertical_speed * (dir_value/abs(dir_value)))
    if is_moving and dir_value % 2 == 1:
      new_x += (self.horizontal_speed * (dir_value/abs(dir_value)))

    if Grid.snap((2, 0))[0] > new_x:
      new_x = pos_x
    if new_x > Grid.snap((7, 0))[0]:
      new_x = pos_x
    if Grid.snap((0, 1.3))[1] > new_y:
      new_y = pos_y
    if new_y > Grid.snap((0, 5.3))[1]:
      new_y = pos_y

    new_position = (new_x, new_y)
    self.position = new_position

  def _start_movement(self, direction):
    self.moving[direction][0] = True

  def _stop_movement(self, direction):
    self.moving[direction][0] = False

class Passenger(LayerItem):
  def __init__(self, x, y):
    super().__init__("passenger", Grid.snap((x,y)))

    self.speed = 0.5

  def update(self):
    pos_x = self.position[0]
    pos_y = self.position[1] + self.speed
    new_position = (pos_x, pos_y + self.speed)

    for k, c in self.layer.items.items():
      if (not self is c) and self.box.has_collided(c.box):
        if c.name == 'player' and (not c.passenger) and pos_x < Grid.snap((7, 0))[0]:
          self.is_active = False
          c.passenger = True
          break

    if pos_y > Grid.snap((0, 8))[1] or pos_y < Grid.snap((0, -2))[1]:
      self.is_active = False
      if "player" in self.layer.items:
        self.layer.items["player"].dropped_passenger = False
    else:
      self.position = new_position

  def update_event(self, event):
    pass

class CarUp(LayerItem):
  def __init__(self, x, y, speed):
    super().__init__("car", Grid.snap((x,y)))
    self.collision_dim = (0.15, -0.05)
    self.speed = speed * (-1)

  def update(self):
    pos_x = self.position[0]
    pos_y = self.position[1] + self.speed
    new_position = (pos_x, pos_y + self.speed)

    # When colliding with other moving cars
    for k, c in self.layer.items.items():
      if (not self is c) and self.box.has_collided(c.box):

        if c.name == 'player':
          self.is_active = False
          continue

        if c.name == 'scoreboard':
          continue

        c_y = c.position[1]
        if pos_y >= c_y:
          new_position = (pos_x, pos_y)
          self.speed = c.speed

    # When going out of bounds
    if pos_y > Grid.snap((0, 8))[1] or pos_y < Grid.snap((0, -2))[1]:
      self.is_active = False
      # self.layer.spawn_car()
    else:
      self.position = new_position

  def update_event(self, event):
    pass
