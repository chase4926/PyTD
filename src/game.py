#!/usr/bin/env python

'''
PyTD: game.py
--------------------------------

Designed around 1280x720 (16:9).
Planned: Will adjust automatically to other resolutions with or without 
scaling.
'''

# System imports
import sys, getopt, time, random, os
# Third party libraries
import yaml
# Pygame imports
import pygame
from pygame.locals import *
# Local library imports
from lib_misc import *
import lib_medialoader as media
# Local Classes
#-

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Load images
media.load_images("../images/")

# Seed with the current time
seed = time.strftime("%y%m%d%H%M%S")
random.seed(seed)

# Pygame setup
pygame.init()

# Various varibles - Default config settings
WIDTH = 1280
HEIGHT = 720
SCALE = True
SMOOTH_SCALE = False
KEEP_ASPECT = True
FULLSCREEN = False
EDITOR = False


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
      EDITOR = True


class GameWindow:
  def __init__(self):
    # Set up the window
    flags = pygame.DOUBLEBUF
    if FULLSCREEN:
      flags = flags | pygame.FULLSCREEN
    self.displaysurf = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    self.displaysurf.fill((0,0,0)) # Background color
    self.drawsurf = pygame.Surface((1280, 720))
    pygame.display.set_caption("PyTD")
    # Scaling
    self.scale_res = get_new_resolution(WIDTH, HEIGHT, 1280, 720, scale=SCALE, keep_aspect=KEEP_ASPECT)
    self.scalesurf = pygame.Surface((self.scale_res[0], self.scale_res[1]))
    # Calculate image panning
    self.pan = ( int(round((WIDTH-self.scale_res[0])/2)), int(round((HEIGHT-self.scale_res[1])/2)) )
    # Disable scaling if it isn't needed
    if self.scale_res == (1280, 720):
      SCALING = False
    # Window object init
    self.clock = pygame.time.Clock()
    self.controller = Controller(self)

  def blit(self, surface, coords):
    self.drawsurf.blit(surface, coords)

  def loop(self):
    self.running = True
    
    while self.running:
      # Keep the game running smoothly
      self.clock.tick(60) # Ticks per second
      # Update the controller
      self.controller.update()
      # Fill with black to get rid of previous blits
      self.drawsurf.fill((0,0,0))
      # Let the controller draw everything
      self.controller.draw()
      # Blit either the scaled image or drawsurf to display
      if SCALE:
        if SMOOTH_SCALE:
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
    #self.world = World()
    #self.mousetooltip = MouseToolTip(self.world)
    #DELETEME---
    self.image = media.get("test.png")
    #---

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
    #DELETEME---
    self.window.blit(self.image, (0,0))
    #---
    #self.world.draw(self.window)
    ## Remove eventually
    #self.mousetooltip.draw(self.window)


#class MouseToolTip:
  #def __init__(self, world):
    #self.world = world
    #self.terrain = world.terrain
    #self.font = pygame.font.Font("freesansbold.ttf", 32)

  #def get_current(self):
    #mousex, mousey = pygame.mouse.get_pos()
    #x = int(round(float(mousex + self.world.terrain_x - 8) / self.terrain.tile_size))
    #y = int(round(float(mousey + self.world.terrain_y - 8) / self.terrain.tile_size))
    #return self.terrain.get(x, y)

  #def draw(self, window):
    #text = self.font.render(self.get_current(), True, (255, 255, 255))
    #window.blit(text, (32, 32))


#class World:
  #def __init__(self):
    #self.terrain = Terrain(width=80, height=160)
    #self.terrain_x = 0
    #self.terrain_y = 0

  #def pan(self, x_offset=0, y_offset=0):
    #self.terrain_x += x_offset
    #self.terrain_y += y_offset

  #def draw(self, window):
    #window.blit(self.terrain.surface, (-self.terrain_x, -self.terrain_y))


# Load config
try:
  with open('../config.yml', 'r') as f:
    CONFIG = yaml.load(f)
  WIDTH = CONFIG.get('width', 1280)
  HEIGHT = CONFIG.get('height', 720)
  SCALE = CONFIG.get('scale', True)
  SMOOTH_SCALE = CONFIG.get('smooth_scale', False)
  KEEP_ASPECT = CONFIG.get('keep_aspect', True)
  FULLSCREEN = CONFIG.get('fullscreen', False)
except FileNotFoundError:
  print("Config file doesn't exist! Using default settings.")
# Parse arguments
parse_options()
# Initialize the window
window = GameWindow()
# Start 'er up!
window.loop()
# Deconstruct all pygame stuff
pygame.quit()

