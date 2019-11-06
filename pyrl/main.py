#!/usr/bin/env python

import tcod
import tcod.console
import tcod.event

from . import config
from .components import Collider, Energy, Fighter, Name, Player, Visual
from .components.action import Action
from .components.ai import player as player_ai
from .esper_ext import RunWhile, WorldExt, debug_world
from .mapgen import generate_monsters, random_map
from .processors import (
    AiProcessor,
    CollisionProcessor,
    FovProcessor,
    InputProcessor,
    MoveAndMeleeProcessor,
    MovementProcessor,
    PonderProcessor,
    RenderProcessor,
    SkipProcessor,
    TimeProcessor,
)
from .resources import Fov, Map, input_action
from .resources.input_action import InputAction, noop


def add_processors(world: WorldExt) -> None:
    world.add_processors(
        InputProcessor(),
        AiProcessor(),
        RunWhile(
            there_are_actions_to_take,
            [
                SkipProcessor(),
                MoveAndMeleeProcessor(),
                CollisionProcessor(),
                MovementProcessor(),
                PonderProcessor(),
            ],
        ),
        TimeProcessor(),
        FovProcessor(),
        RenderProcessor(),
    )


def there_are_actions_to_take(world: WorldExt) -> bool:
    have_input = world.try_resource(InputAction) is not noop
    have_player_action = world.get_components(Action, Player)

    if not have_input and not have_player_action:
        return False
    for ent, (energy, _) in world.get_components(Energy, Action):
        if energy.can_act:
            return True
    return False


def add_player(world: WorldExt) -> None:
    map = world.get_resource(Map)
    world.create_entity(
        map.spawn_position,
        Visual("@", tcod.white),
        player_ai,
        Player(),
        Name("Player"),
        Collider(),
        Energy(1),
        Fighter(hp=30, defense=2, power=5,),
    )


def build_world() -> WorldExt:
    world = WorldExt()
    add_processors(world)

    map = random_map()
    world.add_resource(map)
    world.add_resource(Fov(map))

    add_player(world)
    generate_monsters(world)

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
