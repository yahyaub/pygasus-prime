import pygame
from pygame.locals import *

class TimerCollection:
  def __init__(self):
    self.timers = {}

  def add(self, key:str, seconds:int):
    if seconds <= 0:
      return
    self.timers[key] = Timer(key, seconds)

  def get(self, key:str):
    return self.timers[key]

  def remove(self, key:str):
    del self.timers[key]

  def reset(self, key:str):
    self.timers[key].reset()

  def toggle(self, key:str):
    self.timers[key].toggle()

  def tick_all(self, keep_on:bool=False):
    for k, timer in self.timers.items():
      timer.tick(keep_on)

  def reset_all(self):
    for k, timer in self.timers.items():
      timer.reset()

class Timer:
  def __init__(self, name:str, start_seconds:int):
    self.name = name
    self.start_seconds = start_seconds
    self.now_seconds = start_seconds
    self.last_ticks = pygame.time.get_ticks()
    self.is_on = False

  def tick(self, keep_on:bool=False):
    if(self.is_on):
      latest_ticks = pygame.time.get_ticks()
      latest_seconds = (latest_ticks - self.last_ticks)//1000

      if latest_seconds >= 1:
        self.now_seconds -= 1
        if self.now_seconds <= 0:
          self.reset(keep_on)

      self.last_ticks = pygame.time.get_ticks()

  def reset(self, is_on:bool=False):
    self.now_seconds = self.start_seconds
    self.last_ticks = pygame.time.get_ticks()
    self.is_on = is_on

  def toggle(self):
    if self.start_seconds == 0:
      return
    self.is_on = not self.is_on
