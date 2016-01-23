#!/usr/bin/env python

'''
PyTD: config.py
--------------------------------

Shared global variables.

DO NOT MAKE CHANGES TO THIS FILE! These are the default values, they
are only used when the config.yml file is not found!
'''

# Third party libraries
import yaml


# Various varibles
WIDTH = 1280
HEIGHT = 720
SCALE = True
SMOOTH_SCALE = False
KEEP_ASPECT = True
FULLSCREEN = False
EDITOR = False


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
