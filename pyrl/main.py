#!/usr/bin/env python
import tcod
import tcod.console
import tcod.event

from pyrl import config
from pyrl.esper_ext import WorldExt
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
    StairsProcessor,
    TimeProcessor,
    UseItemProcessor,
)
from pyrl.processors.main_menu import MainMenuProcessor
from pyrl.resources import input_action
from pyrl.resources.menu import main_menu
from pyrl.world_helpers import RunPerActor


def add_processors(world: WorldExt) -> None:
    world.add_processors(
        # Get, handle input
        InputProcessor(),
        InspectProcessor(),
        MenuProcessor(),
        MainMenuProcessor(),
        RunPerActor(
            # Compute the next action
            AiProcessor(),
            # Execute action
            SkipProcessor(),
            MoveAndMeleeProcessor(),
            PickupProcessor(),
            UseItemProcessor(),
            DropProcessor(),
            StairsProcessor(),
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


def build_world() -> WorldExt:
    world = WorldExt()
    add_processors(world)
    world.add_resource(init_tcod())
    world.add_resource(input_action.noop)
    world.add_resource(main_menu)
    return world


def init_tcod():
    tcod.console_set_custom_font(
        str(config.FONT_PATH), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
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


def main():
    world = build_world()
    while not should_quit(world):
        world.process()


if __name__ == "__main__":
    main()
