#!/usr/bin/env python

import tcod
import tcod.console
import tcod.event

from . import config
from .components import Position, Visual
from .components.ai import player as player_ai
from .esper_ext import WorldExt
from .mapgen import dummy_map
from .processors import (AiProcessor, InputProcessor, MovementProcessor,
                         RenderProcessor)
from .resources import input_action


def add_processors(world: WorldExt) -> None:
    world.add_processors(
        InputProcessor(), AiProcessor(), MovementProcessor(), RenderProcessor()
    )


def add_player(world: WorldExt) -> None:
    world.create_entity(
        Position(int(config.SCREEN_WIDTH / 2), int(config.SCREEN_HEIGHT / 2)),
        Visual("@", tcod.white),
        player_ai,
    )


def add_npc(world: WorldExt) -> None:
    world.create_entity(
        Position(int(config.SCREEN_WIDTH / 2 - 5), int(config.SCREEN_WIDTH / 2 - 5)),
        Visual("@", tcod.yellow),
    )


def build_world() -> WorldExt:
    world = WorldExt()
    add_processors(world)
    add_player(world)
    add_npc(world)
    world.add_resource(dummy_map())
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

    while not world.get_resource(input_action.InputAction) is input_action.quit:
        world.process()


if __name__ == "__main__":
    main()
