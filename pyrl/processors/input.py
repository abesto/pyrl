#!/usr/bin/env python

from typing import ClassVar, Dict, Optional

import tcod.event
from tcod.event import EventDispatch, KeyDown, Quit

from pyrl.resources import Menu

from ..esper_ext import Processor, WorldExt
from ..resources.input_action import (
    InputAction,
    Inspect,
    MenuChoice,
    Move,
    dismiss_menu,
    noop,
    open_drop_menu,
    open_inventory,
    pickup,
    quit,
)
from ..vector import Vector

Keymap = Dict[int, InputAction]


normal_keymap: Keymap = {
    # Quit
    tcod.event.K_ESCAPE: quit,
    # Arrow keys
    tcod.event.K_UP: Move.one["n"],
    tcod.event.K_RIGHT: Move.one["e"],
    tcod.event.K_DOWN: Move.one["s"],
    tcod.event.K_LEFT: Move.one["w"],
    # VIM-like
    tcod.event.K_k: Move.one["n"],
    tcod.event.K_j: Move.one["s"],
    tcod.event.K_h: Move.one["w"],
    tcod.event.K_l: Move.one["e"],
    tcod.event.K_y: Move.one["nw"],
    tcod.event.K_u: Move.one["ne"],
    tcod.event.K_b: Move.one["sw"],
    tcod.event.K_n: Move.one["se"],
    # Inventory management
    tcod.event.K_g: pickup,
    tcod.event.K_i: open_inventory,
    tcod.event.K_d: open_drop_menu,
}


menu_keymap: Keymap = {tcod.event.K_ESCAPE: dismiss_menu}


class InputProcessor(Processor):
    def _event_to_action(self, event: tcod.event.Event) -> InputAction:
        if isinstance(event, tcod.event.Quit):
            return quit
        if isinstance(event, tcod.event.KeyDown):
            if self.world.try_resource(Menu) is not None:
                return menu_keymap.get(
                    event.sym, MenuChoice(event.sym - tcod.event.K_a)
                )
            return normal_keymap.get(event.sym, noop)
        if isinstance(event, tcod.event.MouseMotion):
            if event.tile_motion == (0, 0):
                return noop
            return Inspect(Vector(int(event.tile[0]), int(event.tile[1])))
        return noop

    def process(self):
        self.world.add_resource(self._event_to_action(next(tcod.event.wait())))
