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
class Rect:
    x1: int
    y1: int
    w: int
    h: int
    x2: int = field(init=False)
    y2: int = field(init=False)

    def __post_init__(self):
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self) -> Position:
        return Position(int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2))

    def intersect(self, other: "Rect") -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


@dataclass
class Map:
    width: int
    height: int
    rooms: List[Rect] = field(default_factory=lambda: [])
    spawn_position: Position = field(init=False)
    tiles: Tiles = field(init=False)

    def __post_init__(self):
        self.tiles = [
            [Tile.wall() for _ in range(self.height)] for _ in range(self.width)
        ]
