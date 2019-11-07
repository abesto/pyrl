#!/usr/bin/env python

from typing import ClassVar, Dict, Optional

import tcod.event
from tcod.event import EventDispatch, KeyDown, Quit

from ..esper_ext import Processor, WorldExt
from ..resources.input_action import InputAction, Inspect, Move, noop, quit
from ..vector import Vector

Keymap = Dict[int, InputAction]


simple_keymap: Keymap = {
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
}


def event_to_action(event: tcod.event.Event) -> InputAction:
    if isinstance(event, tcod.event.Quit):
        return quit
    if isinstance(event, tcod.event.KeyDown):
        return simple_keymap.get(event.sym, noop)
    if isinstance(event, tcod.event.MouseMotion):
        if event.tile_motion == (0, 0):
            return noop
        return Inspect(Vector(int(event.tile[0]), int(event.tile[1])))
    return noop


class InputProcessor(Processor):
    def process(self):
        self.world.add_resource(event_to_action(next(tcod.event.wait())))
