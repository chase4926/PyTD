#!/usr/bin/env python

'''
PyTD: game.py
--------------------------------

Designed around 1280x720 (16:9).
'''

# System imports
import sys, getopt, time, random, os
# Third party libraries
import yaml
# Pygame imports
import pygame
from pygame.locals import *

# Make sure we're in the right directory before importing locally
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Local library imports
from lib_misc import *
import lib_medialoader as media
# Local Modules
import config
import editor

# Load images
media.load_images("../images/")

# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()


def force_close():
  pygame.quit()
  sys.exit(2)

def parse_options():
  try:
    opts, args = getopt.getopt(sys.argv[1:],"he",["help", "editor"])
  except getopt.GetoptError:
    force_close()
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print("\nUsage: game.py {arg}\n\n-h / --help\tThe screen you are viewing now\n-e / --editor\tLevel Editor")
      force_close()
    elif opt in ("-e", "--editor"):
      config.EDITOR = True


class GameWindow:
  def __init__(self):
    # Set up the window
    flags = pygame.DOUBLEBUF
    if config.FULLSCREEN:
      flags = flags | pygame.FULLSCREEN
    self.displaysurf = pygame.display.set_mode((config.WIDTH, config.HEIGHT), flags)
    self.displaysurf.fill((0,0,0)) # Background color
    self.drawsurf = pygame.Surface((1280, 720))
    # Scaling
    self.scale_res = get_new_resolution(config.WIDTH, config.HEIGHT,
                                        1280, 720, scale=config.SCALE,
                                        keep_aspect=config.KEEP_ASPECT)
    self.scalesurf = pygame.Surface((self.scale_res[0], self.scale_res[1]))
    # Calculate image panning
    self.pan = ( int(round((config.WIDTH-self.scale_res[0])/2)), int(round((config.HEIGHT-self.scale_res[1])/2)) )
    # Disable scaling if it isn't needed
    if self.scale_res == (1280, 720):
      config.SCALE = False
    # Window object init
    self.clock = pygame.time.Clock()
    if config.EDITOR:
      pygame.display.set_caption("PyTD - EDITOR")
      self.controller = editor.Controller(self)
    else:
      pygame.display.set_caption("PyTD")
      self.controller = Controller(self)

  def get_fps(self):
    return self.clock.get_fps()

  def close(self):
    self.running = False

  def get_mouse_pos(self):
    # This returns (mouse_x,mouse_y) adjusted for window settings
    mousex, mousey = pygame.mouse.get_pos()
    if config.SCALE:
      # Must adjust for panning and then adjust for the scale
      return (round(((mousex-self.pan[0])*1280)/self.scale_res[0]),
              round(((mousey-self.pan[1])* 720)/self.scale_res[1]))
    else:
      # Must only adjust for panning
      # This method is much faster and more accurate
      return mousex-self.pan[0], mousey-self.pan[1]

  def blit(self, surface, coords):
    self.drawsurf.blit(surface, coords)

  def loop(self):
    self.running = True
    
    while self.running:
      # Keep the game running smoothly
      self.clock.tick(60) # Ticks per second
      # Handle events and distribute key presses
      for event in pygame.event.get():
        if event.type == QUIT:
          self.close()
        if event.type == KEYDOWN:
          self.controller.key_pressed(event.key)
      # Update the controller
      self.controller.update()
      # Fill with black to get rid of previous blits
      self.drawsurf.fill((0,0,0))
      # Let the controller draw everything
      self.controller.draw()
      # Blit either the scaled image or drawsurf to display
      if config.SCALE:
        if config.SMOOTH_SCALE:
          pygame.transform.smoothscale(self.drawsurf, self.scale_res, self.scalesurf)
        else:
          pygame.transform.scale(self.drawsurf, self.scale_res, self.scalesurf)
        self.displaysurf.blit(self.scalesurf, self.pan)
      else:
        self.displaysurf.blit(self.drawsurf, self.pan)
      # "Flip" the display
      pygame.display.update()


class Controller:
  def __init__(self, window):
    self.window = window
    #DELETEME---
    self.image = media.get("test.png").convert()
    #---

  def key_pressed(self, key):
    if key == K_ESCAPE:
      self.window.close()

  def update(self):
    ## Key is down (Holding down a key will keep triggering)
    #keys_pressed = pygame.key.get_pressed()
    pass

  def draw(self):
    # All the draws:
    #DELETEME---
    self.window.blit(self.image, (0,0))
    #---


# Parse arguments
parse_options()
# Initialize the window
window = GameWindow()
# Start 'er up!
window.loop()
# Deconstruct all pygame stuff
pygame.quit()

