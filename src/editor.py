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
  # This is the controller used for the editor, not the game itself
  def __init__(self, window):
    self.window = window
    self.editor = Editor(self.window)

  def key_pressed(self, key):
    if key == K_ESCAPE:
      self.window.close()
    self.editor.key_pressed(key)

  def update(self):
    ## Key is down (Holding down a key will keep triggering)
    #keys_pressed = pygame.key.get_pressed()
    self.editor.update()

  def draw(self):
    # All the draws:
    self.editor.draw()


class Editor:
  def __init__(self, window):
    self.window = window
    self.mode = 0 # 0 = No mode, 1 = City mode, 2 = Route mode
    self.load_level("level0")
    # Font
    self.font = pygame.font.Font("freesansbold.ttf", 32)
    # City Mode
    self.city_surf = pygame.Surface((1280, 720))
    self.city_color = (255, 0, 0)
    self.city_size = 100
    self.redraw_city()

  def redraw_city(self):
    purple = (255, 0, 255)
    # Fill with purple (the transparency color)
    self.city_surf.fill(purple)
    pygame.draw.circle(self.city_surf, self.city_color,
                       self.window.get_mouse_pos(), self.city_size)
    self.city_surf.set_colorkey(purple)

  def load_level(self, level_name):
    # Convert the first layer to make it faster to blit!
    self.layer0 = media.get("levels/{}/layer0.png".format(level_name)).convert()
    self.layer1 = media.get("levels/{}/layer1.png".format(level_name)).convert_alpha()

  def change_mode(self, mode):
    if mode == 0:
      self.mode = 0
      pygame.display.set_caption("PyTD - EDITOR")
    elif mode == 1:
      self.mode = 1
      pygame.display.set_caption("PyTD - EDITOR -- City Mode")
    elif mode == 2:
      self.mode = 2
      pygame.display.set_caption("PyTD - EDITOR -- Route Mode")

  def key_pressed(self, key):
    if key == K_SPACE:
      print(self.window.get_mouse_pos())
    elif key == K_F1:
      config.SMOOTH_SCALE = not config.SMOOTH_SCALE
    elif key == K_1:
      # City placement mode
      if self.mode == 1:
        self.change_mode(0)
      else:
        self.change_mode(1)
    elif key == K_2:
      # Route placement mode
      if self.mode == 2:
        self.change_mode(0)
      else:
        self.change_mode(2)

  def update(self):
    self.redraw_city()
    #pass

  def draw(self):
    self.window.blit(self.layer0, (0,0))
    self.window.blit(self.layer1, (0,0))
    self.window.blit(self.city_surf, (0,0))
    self.window.blit(self.font.render(str(self.window.get_fps()), True, (255, 255, 255)), (32,32))

