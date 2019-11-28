#!/usr/bin/env python

from typing import ClassVar, Dict, Optional

import tcod.event
from tcod.event import EventDispatch, KeyDown, Quit

from pyrl.resources import Menu, Targeting

from ..esper_ext import Processor, WorldExt
from ..resources.input_action import (
    InputAction,
    Inspect,
    MenuChoice,
    Move,
    UseFromInventory,
    cancel_targeting,
    dismiss_menu,
    noop,
    open_drop_menu,
    open_inventory,
    pickup,
    quit,
    quit_to_main_menu,
)
from ..vector import Vector

Keymap = Dict[int, InputAction]


normal_keymap: Keymap = {
    # Quit
    tcod.event.K_ESCAPE: quit_to_main_menu,
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


targeting_keymap: Keymap = {tcod.event.K_ESCAPE: cancel_targeting}


class InputProcessor(Processor):
    def __init__(self):
        self._buffered_event: Optional[tcod.event.Event] = None

    def _event_to_action(self, event: tcod.event.Event) -> InputAction:
        if isinstance(event, tcod.event.Quit):
            # Hey look, save scumming opportunity!
            return quit

        if isinstance(event, tcod.event.KeyDown):
            if self.world.try_resource(Menu) is not None:
                return menu_keymap.get(
                    event.sym, MenuChoice(event.sym - tcod.event.K_a)
                )

            targeting = self.world.try_resource(Targeting)
            if targeting is not None:
                return targeting_keymap.get(event.sym, noop)

            return normal_keymap.get(event.sym, noop)

        if isinstance(event, tcod.event.MouseMotion):
            if event.tile_motion == (0, 0):
                return noop
            if self.world.try_resource(Menu) is not None:
                return noop

            vector = Vector(int(event.tile.x), int(event.tile.y))
            targeting = self.world.try_resource(Targeting)
            if targeting is not None:
                self.world.add_resource(targeting.with_current_target(vector))
            return Inspect(vector)

        if isinstance(event, tcod.event.MouseButtonDown):
            if event.button != tcod.event.BUTTON_LEFT:
                return noop

            targeting = self.world.try_resource(Targeting)
            if targeting is None:
                return noop

            self.world.remove_resource(Targeting)
            return UseFromInventory(
                targeting.for_inventory_index,
                Vector(int(event.tile.x), int(event.tile.y)),
            )

        return noop

    def _process(self, event) -> None:
        self.world.add_resource(self._event_to_action(event))

    def process(self):
        if self._buffered_event:
            event, self._buffered_event = self._buffered_event, None
            return self._process(event)

        last_mouse_motion: Optional[tcod.event.MouseMotion] = None
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.MouseMotion):
                last_mouse_motion = event
                continue
            elif last_mouse_motion is None:
                return self._process(event)
            else:
                self._buffered_event = event
                return self._process(last_mouse_motion)
        if last_mouse_motion:
            self._process(last_mouse_motion)
