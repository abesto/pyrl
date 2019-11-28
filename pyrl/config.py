#!/usr/bin/env python

import os
from dataclasses import dataclass
from pathlib import Path

from appdirs import user_data_dir
from tcod.color import Color

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

ASSETS_DIR = Path("assets")
FONT_PATH = ASSETS_DIR / "arial10x10.png"
MAIN_MENU_BACKGROUND_PATH = ASSETS_DIR / "menu_background1.png"

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MESSAGE_X = BAR_WIDTH + 2
MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MESSAGE_HEIGHT = PANEL_HEIGHT - 1

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT

INVENTORY_WIDTH = 50

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

DATADIR = Path(user_data_dir("pyrl", "abesto"))
SAVEFILE = DATADIR / "save.dat"


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
