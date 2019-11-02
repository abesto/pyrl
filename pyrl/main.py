#!/usr/bin/env python

import tcod
import tcod.console
import tcod.event

from . import config
from .components import Player, Position, Visual
from .components.ai import player as player_ai
from .esper_ext import WorldExt
from .mapgen import random_map
from .processors import (AiProcessor, CollisionProcessor, FovProcessor,
                         InputProcessor, MoveAndMeleeProcessor,
                         MovementProcessor, RenderProcessor)
from .resources import Fov, Map, input_action


def add_processors(world: WorldExt) -> None:
    world.add_processors(
        InputProcessor(),
        AiProcessor(),
        MoveAndMeleeProcessor(),
        CollisionProcessor(),
        MovementProcessor(),
        FovProcessor(),
        RenderProcessor(),
    )


def add_player(world: WorldExt) -> None:
    map = world.get_resource(Map)
    world.create_entity(
        map.spawn_position, Visual("@", tcod.white), player_ai, Player()
    )


def add_npc(world: WorldExt) -> None:
    world.create_entity(
        Position(int(config.SCREEN_WIDTH / 2 - 5), int(config.SCREEN_WIDTH / 2 - 5)),
        Visual("@", tcod.yellow),
    )


def build_world() -> WorldExt:
    world = WorldExt()
    add_processors(world)

    map = random_map()
    world.add_resource(map)
    world.add_resource(Fov(map))

    add_player(world)
    add_npc(world)
    return world


def init_tcod():
    tcod.console_set_custom_font(
        config.FONT_PATH, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )

    root = tcod.console_init_root(
        config.SCREEN_WIDTH,
        config.SCREEN_HEIGHT,
        "libtcod tutorial but with ECS",
        fullscreen=False,
        renderer=tcod.RENDERER_OPENGL2,
        vsync=True,
    )

    return root


def main():
    world = build_world()

    world.add_resource(init_tcod())
    world.add_resource(input_action.noop)

    while world.get_resource(input_action.InputAction) is not input_action.quit:
        world.process()


if __name__ == "__main__":
    main()
