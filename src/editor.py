#!/usr/bin/env python

'''
PyTD: editor.py
--------------------------------

This will be a basic level editor, seeing as a level editor is barely
needed for this project.
'''

# Pygame imports
import pygame
from pygame.locals import *


class Controller:
  def __init__(self, window):
    self.window = window
    #self.world = World()
    #self.mousetooltip = MouseToolTip(self.world)

  def update(self):
    # Key is down (Holding down a key will keep triggering)
    keys_pressed = pygame.key.get_pressed()
    #if keys_pressed[pygame.K_DOWN]:
      #self.world.pan(y_offset=4)
    #if keys_pressed[pygame.K_UP]:
      #self.world.pan(y_offset=-4)
    # Key presses (Holding down a key will only trigger once)
    for event in pygame.event.get():
        if event.type == QUIT:
          self.window.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.window.running = False

  def draw(self):
    # All the draws:
    pass
    #self.world.draw(self.window)
    ## Remove eventually
    #self.mousetooltip.draw(self.window)


class Editor:
  def __init__(self):
    self.terrain = Terrain(width=80, height=160)
    self.terrain_x = 0
    self.terrain_y = 0

  def pan(self, x_offset=0, y_offset=0):
    self.terrain_x += x_offset
    self.terrain_y += y_offset

  def draw(self, window):
    window.blit(self.terrain.surface, (-self.terrain_x, -self.terrain_y))

