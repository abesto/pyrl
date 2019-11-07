#!/usr/bin/env python

import tcod
import tcod.console
import tcod.event

from pyrl import config
from pyrl.components import Collider, Energy, Fighter, Inventory, Name, Player, Visual
from pyrl.components.ai import player as player_ai
from pyrl.components.visual import RenderOrder
from pyrl.esper_ext import WorldExt
from pyrl.mapgen import generate_items, generate_monsters, random_map
from pyrl.processors import (
    AiProcessor,
    CollisionProcessor,
    DropProcessor,
    FovProcessor,
    InputProcessor,
    InspectProcessor,
    MenuProcessor,
    MonsterDeathProcessor,
    MoveAndMeleeProcessor,
    MovementProcessor,
    PickupProcessor,
    PlayerDeathProcessor,
    PonderProcessor,
    RenderProcessor,
    SkipProcessor,
    TimeProcessor,
    UseItemProcessor,
)
from pyrl.resources import Fov, Map, Messages, input_action
from pyrl.world_helpers import RunPerActor


def add_processors(world: WorldExt) -> None:
    world.add_processors(
        # Get, handle input
        InputProcessor(),
        InspectProcessor(),
        MenuProcessor(),
        RunPerActor(
            # Compute the next action
            AiProcessor(),
            # Execute action
            SkipProcessor(),
            MoveAndMeleeProcessor(),
            PickupProcessor(),
            UseItemProcessor(),
            DropProcessor(),
            # Compute results
            CollisionProcessor(),
            MovementProcessor(),
            PonderProcessor(),
            PlayerDeathProcessor(),
            MonsterDeathProcessor(),
        ),
        TimeProcessor(),
        FovProcessor(),
        RenderProcessor(),
    )


def add_player(world: WorldExt) -> None:
    map = world.get_resource(Map)
    world.create_entity(
        map.spawn_position,
        Visual("@", tcod.white, RenderOrder.Actor),
        player_ai,
        Player(),
        Name("Player"),
        Collider(),
        Energy(1),
        Fighter.new(hp=30, defense=2, power=5,),
        Inventory(26),
    )


def build_world() -> WorldExt:
    world = WorldExt()
    add_processors(world)

    map = random_map()
    world.add_resource(map)
    world.add_resource(Fov(map))
    world.add_resource(Messages(5))

    add_player(world)
    generate_monsters(world)
    generate_items(world)

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


def should_quit(world: WorldExt) -> bool:
    return world.get_resource(input_action.InputAction) is input_action.quit


def player_alive(world: WorldExt) -> bool:
    for _, (_, fighter) in world.get_components(Player, Fighter):
        if fighter.alive:
            return True
    return False


def main():
    world = build_world()

    world.add_resource(init_tcod())
    world.add_resource(input_action.noop)

    while not should_quit(world) and player_alive(world):
        world.process()


if __name__ == "__main__":
    main()
