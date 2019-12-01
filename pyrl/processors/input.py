#!/usr/bin/env python

from typing import Dict, Optional, Tuple, Union

import tcod.event

from pyrl.resources import Menu, Targeting

from ..esper_ext import Processor
from ..resources.input_action import (
    InputAction,
    Inspect,
    MenuChoice,
    Move,
    UseFromInventory,
    cancel_targeting,
    dismiss_menu,
    noop,
    open_character_menu,
    open_drop_menu,
    open_inventory,
    pickup,
    quit,
    quit_to_main_menu,
    take_stairs,
)
from ..vector import Vector

Keymap = Dict[Union[int, Tuple[int, int]], InputAction]


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
    # Down we go,
    (tcod.event.K_PERIOD, tcod.event.KMOD_SHIFT): take_stairs,
    # Inventory management
    tcod.event.K_g: pickup,
    tcod.event.K_i: open_inventory,
    tcod.event.K_d: open_drop_menu,
    # Character screen!
    tcod.event.K_c: open_character_menu,
}


menu_keymap: Keymap = {tcod.event.K_ESCAPE: dismiss_menu}


targeting_keymap: Keymap = {tcod.event.K_ESCAPE: cancel_targeting}


def keymap_lookup(
    keymap: Keymap, event: tcod.event.KeyboardEvent
) -> Optional[InputAction]:
    # Easy case: exact match with no modifiers
    if event.mod == 0 and event.sym in keymap:
        return keymap[event.sym]
    # Hard case: we have modifiers, so we need to iterate, because for example SHIFT
    # matches both LSHIFT and RSHIFT.
    # To optimize, could pre-process the keymap, but meh.
    for binding, action in keymap.items():
        if isinstance(binding, int):
            continue
        sym, mod = binding
        if sym == event.sym and event.mod & mod:
            return action
    return None


class InputProcessor(Processor):
    def __init__(self):
        self._buffered_event: Optional[tcod.event.Event] = None

    def _event_to_action(self, event: tcod.event.Event) -> InputAction:
        if isinstance(event, tcod.event.Quit):
            # Hey look, save scumming opportunity!
            return quit

        if isinstance(event, tcod.event.KeyDown):
            if self.world.try_resource(Menu) is not None:
                return keymap_lookup(menu_keymap, event) or MenuChoice(
                    event.sym - tcod.event.K_a
                )

            targeting = self.world.try_resource(Targeting)
            if targeting is not None:
                return keymap_lookup(targeting_keymap, event) or noop

            return keymap_lookup(normal_keymap, event) or noop

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
