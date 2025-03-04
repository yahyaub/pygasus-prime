import pygame, pytest

from packages.time.timer import Timer, TimerCollection

pygame.init()

class TestTimer():
  def test_timer_can_toggle(self):
    timer = Timer('timer-a', 1)
    timer.toggle()
    is_on = timer.is_on
    timer.toggle()
    is_off = timer.is_on

    assert is_on == True and is_off == False

  def test_timer_can_tick(self):
    timer = Timer('timer-a', 1)
    timer.toggle()

    last_ticks = timer.last_ticks
    pygame.time.wait(100)
    timer.tick()

    assert timer.last_ticks > last_ticks

  def test_timer_can_countdown(self):
    timer = Timer('timer-a', 2)
    timer.toggle()

    pygame.time.wait(1000)
    timer.tick()

    assert timer.now_seconds == 1

  def test_timer_reset_after_countdown(self):
    timer = Timer('timer-a', 2)
    timer.toggle()

    pygame.time.wait(1000)
    timer.tick()
    pygame.time.wait(1000)
    timer.tick()
    pygame.time.wait(1000)
    timer.tick()

    assert timer.now_seconds == 2

  def test_timer_restarts_after_countdown(self):
    timer = Timer('timer-a', 2)
    timer.toggle()

    pygame.time.wait(1000)
    timer.tick(True)
    pygame.time.wait(1000)
    timer.tick(True)
    pygame.time.wait(1000)
    timer.tick(True)

    assert timer.now_seconds == 1

  def test_timer_cannot_countdown_from_zero(self):
    timer = Timer('timer-a', 0)
    timer.toggle()

    assert timer.is_on == False

class TestTimerCollection():
  
  @pytest.fixture(autouse=True)
  def setup_timer_collection(self):
    self.timer_collection = TimerCollection()

  def test_new_collection_has_no_timers(self):
    assert len(self.timer_collection.timers) == 0

  def test_collection_can_add(self):
    self.timer_collection.add('t1', 2)
    assert len(self.timer_collection.timers) == 1
  
  def test_collection_cannot_add_zero_timers(self):
    self.timer_collection.add('t1', 0)
    assert len(self.timer_collection.timers) == 0

  def test_collection_can_get(self):
    self.timer_collection.add('t1', 1)
    self.timer_collection.add('t2', 2)
    t2 = self.timer_collection.get('t2')
    assert t2.start_seconds == 2 and len(self.timer_collection.timers) == 2

  def test_collection_can_remove(self):
    self.timer_collection.add('t1', 1)
    self.timer_collection.add('t2', 2)
    self.timer_collection.remove('t1')
    t2 = self.timer_collection.get('t2')
    assert t2.start_seconds == 2 and len(self.timer_collection.timers) == 1

  def test_collection_can_tick_timers(self):
    self.timer_collection.add('t1', 1)
    self.timer_collection.add('t2', 2)

    self.timer_collection.toggle('t1')
    t1_last_ticks = self.timer_collection.get('t1').last_ticks
    pygame.time.wait(100)
    self.timer_collection.tick_all()

    self.timer_collection.toggle('t2')
    t2_last_ticks = self.timer_collection.get('t2').last_ticks
    pygame.time.wait(100)
    self.timer_collection.tick_all()

    assert (self.timer_collection.get('t1').last_ticks > t1_last_ticks) and (self.timer_collection.get('t2').last_ticks > t2_last_ticks)

  def test_collection_can_reset_timer(self):
    self.timer_collection.add('t1', 2)
    self.timer_collection.toggle('t1')
    pygame.time.wait(1000)
    self.timer_collection.tick_all()
    seconds = self.timer_collection.get('t1').now_seconds
    self.timer_collection.reset('t1')
    assert (seconds == 1) and (self.timer_collection.get('t1').now_seconds == 2)

  def test_collection_can_reset_all_timers(self):
    self.timer_collection.add('t1', 2)
    self.timer_collection.add('t2', 3)
    self.timer_collection.toggle('t1')
    self.timer_collection.toggle('t2')

    pygame.time.wait(1000)
    self.timer_collection.tick_all()
    t1_seconds = self.timer_collection.get('t1').now_seconds
    t2_seconds = self.timer_collection.get('t2').now_seconds
    self.timer_collection.reset_all()

    t1_timer_reset = (t1_seconds == 1) and (self.timer_collection.get('t1').now_seconds == 2)
    t2_timer_reset = (t2_seconds == 2) and (self.timer_collection.get('t2').now_seconds == 3)
    assert t1_timer_reset and t2_timer_reset

