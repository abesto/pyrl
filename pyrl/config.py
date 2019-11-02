#!/usr/bin/env python

import os
from dataclasses import dataclass

from tcod.color import Color

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FONT_PATH = os.path.join("assets", "arial10x10.png")

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30


@dataclass
class Theme:
    dark_wall: Color
    dark_ground: Color


theme = Theme(dark_wall=Color(0, 0, 100), dark_ground=Color(50, 50, 150))
