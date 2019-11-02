#!/usr/bin/env python

from dataclasses import dataclass, field
from typing import List

from ..components import Position


@dataclass
class Tile:
    blocked: bool
    block_sight: bool = None  # type: ignore
    explored: bool = False

    def __post_init__(self):
        if self.block_sight is None:
            self.block_sight = self.blocked

    @classmethod
    def floor(cls):
        return cls(blocked=False)

    @classmethod
    def wall(cls):
        return cls(blocked=True)


Tiles = List[List[Tile]]


@dataclass
class Map:
    width: int
    height: int
    spawn_position: Position = field(init=False)
    tiles: Tiles = field(init=False)

    def __post_init__(self):
        self.tiles = [
            [Tile.wall() for _ in range(self.height)] for _ in range(self.width)
        ]
