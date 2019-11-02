#!/usr/bin/env python

from dataclasses import InitVar, dataclass, field

import tcod.map

from .map import Map


@dataclass
class Fov:
    map: InitVar[Map]
    should_recompute: bool = True
    fov_map: tcod.map.Map = field(init=False)

    def __post_init__(self, map: Map):
        self.fov_map = tcod.map.Map(map.width, map.height)
        for y in range(map.height):
            for x in range(map.width):
                self.fov_map.transparent[y, x] = not map.tiles[x][y].block_sight
                self.fov_map.walkable[y, x] = not map.tiles[x][y].blocked
