#!/usr/bin/env python

from . import config
from .resources.map import Map, Tile


def dummy_map() -> Map:
    map = Map(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
    for x, y in ((30, 22), (31, 22), (32, 22)):
        map.tiles[x][y].blocked = True
        map.tiles[x][y].block_sight = True
    return map
