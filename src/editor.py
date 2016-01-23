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
# Local library imports
import lib_medialoader as media
# Local Modules
import config


class Controller:
  def __init__(self, window):
    self.window = window
    self.editor = Editor()

  def update(self):
    # Key is down (Holding down a key will keep triggering)
    keys_pressed = pygame.key.get_pressed()
    # Key presses (Holding down a key will only trigger once)
    for event in pygame.event.get():
        if event.type == QUIT:
          self.window.running = False
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.window.running = False
          elif event.key == K_SPACE:
            print(self.window.get_mouse_pos())
          elif event.key == K_F1:
            config.SMOOTH_SCALE = not config.SMOOTH_SCALE

  def draw(self):
    # All the draws:
    pass
    self.editor.draw(self.window)


class Editor:
  def __init__(self):
    self.load_level("level0")

  def load_level(self, level_name):
    self.layer0 = media.get("levels/{}/layer0.png".format(level_name))
    self.layer1 = media.get("levels/{}/layer1.png".format(level_name))

  def draw(self, window):
    window.blit(self.layer0, (0,0))
    window.blit(self.layer1, (0,0))

