#!/usr/bin/env python

import os
from dataclasses import dataclass

from tcod.color import Color

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FONT_PATH = os.path.join("assets", "arial10x10.png")


@dataclass
class Theme:
    dark_wall: Color
    dark_ground: Color


theme = Theme(dark_wall=Color(0, 0, 100), dark_ground=Color(50, 50, 150))
