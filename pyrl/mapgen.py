#!/usr/bin/env python
from random import randint

import tcod.color

from pyrl.components import Inventory, Player, Stairs
from pyrl.components.item import Item
from pyrl.components.visual import RenderOrder
from pyrl.resources import Fov

from . import config
from .components import Collider, Energy, Fighter, Name, Position, Visual
from .components.ai import basic as basic_ai
from .components.ai import player as player_ai
from .esper_ext import WorldExt
from .resources.map import Map, Rect
from .vector import Vector


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
    map = Map(width=config.MAP_WIDTH, height=config.MAP_HEIGHT, dungeon_level=0)
    create_room(map, Rect(20, 15, 10, 15))
    create_room(map, Rect(35, 15, 10, 15))
    create_h_tunnel(map, 25, 40, 23)
    return map


def random_map(dungeon_level: int) -> Map:
    map = Map(
        width=config.MAP_WIDTH, height=config.MAP_HEIGHT, dungeon_level=dungeon_level
    )

    for _ in range(config.MAX_ROOMS):
        # random width and height
        w = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        h = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = randint(0, map.width - w - 1)
        y = randint(0, map.height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        if not any(new_room.intersect(other_room) for other_room in map.rooms):
            create_room(map, new_room)
            new_center = new_room.center
            if not map.rooms:
                map.spawn_position = Position(new_center)
            else:
                connect_room(map, new_center)
            map.rooms.append(new_room)

    return map


def connect_room(map: Map, new_center: Vector) -> None:
    # center coordinates of previous room
    prev_center = map.rooms[-1].center
    # flip a coin (random number that is either 0 or 1)
    if randint(0, 1) == 1:
        # first move horizontally, then vertically
        create_h_tunnel(map, prev_center.x, new_center.x, prev_center.y)
        create_v_tunnel(map, prev_center.y, new_center.y, new_center.x)
    else:
        # first move vertically, then horizontally
        create_v_tunnel(map, prev_center.y, new_center.y, prev_center.x)
        create_h_tunnel(map, prev_center.x, new_center.x, new_center.y)


def generate_monsters(world: WorldExt) -> None:
    map = world.get_resource(Map)

    for room in map.rooms:
        number_of_monsters = randint(0, config.MAX_MONSTERS_PER_ROOM)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            position = Position(
                Vector(
                    x=randint(room.x1 + 1, room.x2 - 1),
                    y=randint(room.y1 + 1, room.y2 - 1),
                )
            )

            if not any(match[1] == position for match in world.get_component(Position)):
                monster = world.create_entity(position, Collider(), Energy(1), basic_ai)
                if randint(0, 100) < 80:
                    world.add_components(
                        monster,
                        Visual(
                            char="o",
                            color=tcod.desaturated_green,
                            render_order=RenderOrder.ACTOR,
                        ),
                        Name("Orc"),
                        Fighter.new(hp=10, defense=0, power=3),
                    )
                else:
                    world.add_components(
                        monster,
                        Visual(
                            char="T",
                            color=tcod.darker_green,
                            render_order=RenderOrder.ACTOR,
                        ),
                        Name("Troll"),
                        Fighter.new(hp=16, defense=1, power=4),
                    )


def generate_items(world: WorldExt) -> None:
    map = world.get_resource(Map)

    for room in map.rooms:
        number_of_items = randint(0, config.MAX_ITEMS_PER_ROOM)

        for i in range(number_of_items):
            position = Position(
                Vector(
                    x=randint(room.x1 + 1, room.x2 - 1),
                    y=randint(room.y1 + 1, room.y2 - 1),
                )
            )

            if not any(match[1] == position for match in world.get_component(Position)):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    world.create_entity(
                        position,
                        Visual("!", tcod.violet, RenderOrder.ITEM),
                        Name("Healing Potion"),
                        Item.HEALING_POTION,
                    )
                elif item_chance < 80:
                    world.create_entity(
                        position,
                        Visual("#", tcod.red, RenderOrder.ITEM),
                        Name("Fireball Scroll"),
                        Item.FIREBALL_SCROLL,
                    )
                elif item_chance < 90:
                    world.create_entity(
                        position,
                        Visual("#", tcod.yellow, RenderOrder.ITEM),
                        Name("Lightning Scroll"),
                        Item.LIGHTNING_SCROLL,
                    )
                else:
                    world.create_entity(
                        position,
                        Visual("#", tcod.purple, RenderOrder.ITEM),
                        Name("Confusion Scroll"),
                        Item.CONFUSION_SCROLL,
                    )


def generate_stairs(world: WorldExt) -> None:
    map = world.get_resource(Map)
    last_room = map.rooms[-1]
    world.create_entity(
        Stairs(map.dungeon_level + 1),
        Position(last_room.center),
        Visual(">", tcod.white, RenderOrder.STAIRS),
        Name("Stairs"),
    )


def add_player(world) -> None:
    map = world.get_resource(Map)
    world.create_entity(
        map.spawn_position,
        Visual("@", tcod.white, RenderOrder.ACTOR),
        player_ai,
        Player(),
        Name("Player"),
        Collider(),
        Energy(1),
        Fighter.new(hp=30, defense=2, power=5,),
        Inventory(26),
    )


def generate_level(world: WorldExt, dungeon_level: int = 1) -> None:
    map = random_map(dungeon_level)
    world.add_resource(map)
    world.add_resource(Fov(map))
    generate_monsters(world)
    generate_items(world)
    generate_stairs(world)
