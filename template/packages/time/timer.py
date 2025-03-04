import pygame
from pygame.locals import *

class TimerCollection:
  def __init__(self):
    self.timers = {}

  def add(self, key, seconds):
    if seconds <= 0:
      return
    self.timers[key] = Timer(key, seconds)

  def get(self, key):
    return self.timers[key]

  def remove(self, key):
    del self.timers[key]

  def reset(self, key):
    self.timers[key].reset()

  def toggle(self, key):
    self.timers[key].toggle()

  def tick_all(self, keep_on=False):
    for k, timer in self.timers.items():
      timer.tick(keep_on)

  def reset_all(self):
    for k, timer in self.timers.items():
      timer.reset()

class Timer:
  def __init__(self, name, start_seconds):
    self.name = name
    self.start_seconds = start_seconds
    self.now_seconds = start_seconds
    self.last_ticks = pygame.time.get_ticks()
    self.is_on = False

  def tick(self, keep_on=False):
    if(self.is_on):
      latest_ticks = pygame.time.get_ticks()
      latest_seconds = (latest_ticks - self.last_ticks)//1000

      if latest_seconds >= 1:
        self.now_seconds -= 1
        if self.now_seconds <= 0:
          self.reset(keep_on)

      self.last_ticks = pygame.time.get_ticks()

  def reset(self, is_on=False):
    self.now_seconds = self.start_seconds
    self.last_ticks = pygame.time.get_ticks()
    self.is_on = is_on

  def toggle(self):
    if self.start_seconds == 0:
      return
    self.is_on = not self.is_on
