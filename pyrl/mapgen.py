#!/usr/bin/env python
from dataclasses import dataclass, field
from random import randint
from typing import List

from . import config
from .components import Position
from .resources.map import Map


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


def create_room(map: Map, room: Rect) -> None:
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map.tiles[x][y].blocked = False

            map.tiles[x][y].block_sight = False


def create_h_tunnel(map: Map, x1: int, x2: int, y: int) -> None:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map.tiles[x][y].blocked = False
        map.tiles[x][y].block_sight = False


def create_v_tunnel(map: Map, y1: int, y2: int, x: int):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map.tiles[x][y].blocked = False
        map.tiles[x][y].block_sight = False


def dummy_map() -> Map:
    map = Map(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
    create_room(map, Rect(20, 15, 10, 15))
    create_room(map, Rect(35, 15, 10, 15))
    create_h_tunnel(map, 25, 40, 23)
    return map


def random_map() -> Map:
    map = Map(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)

    rooms: List[Rect] = []

    for _ in range(config.MAX_ROOMS):
        # random width and height
        w = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        h = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = randint(0, map.width - w - 1)
        y = randint(0, map.height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        if not any(new_room.intersect(other_room) for other_room in rooms):
            create_room(map, new_room)
            new_center = new_room.center
            if not rooms:
                map.spawn_position = new_center
            else:
                # center coordinates of previous room
                prev_center = rooms[-1].center

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(map, prev_center.x, new_center.x, prev_center.y)
                    create_v_tunnel(map, prev_center.y, new_center.y, new_center.x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(map, prev_center.y, new_center.y, prev_center.x)
                    create_h_tunnel(map, prev_center.x, new_center.x, new_center.y)
            rooms.append(new_room)

    return map
