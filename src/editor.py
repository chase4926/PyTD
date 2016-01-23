#!/usr/bin/env python

'''
PyTD: editor.py
--------------------------------

This will be a basic level editor, seeing as a level editor is barely
needed for this project.
'''


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

