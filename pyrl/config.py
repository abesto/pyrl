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

MAX_MONSTERS_PER_ROOM = 3

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10


@dataclass
class Theme:
    dark_wall: Color
    dark_ground: Color
    light_wall: Color
    light_ground: Color

    def background_color(self, wall: bool, visible: bool) -> Color:
        if visible:
            if wall:
                return self.light_wall
            else:
                return self.light_ground
        else:
            if wall:
                return self.dark_wall
            else:
                return self.dark_ground


theme = Theme(
    dark_wall=Color(0, 0, 100),
    dark_ground=Color(50, 50, 150),
    light_wall=Color(130, 110, 50),
    light_ground=Color(200, 180, 50),
)
