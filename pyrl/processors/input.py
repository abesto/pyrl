#!/usr/bin/env python

from typing import ClassVar, Dict, Optional

import tcod.event
from tcod.event import EventDispatch, KeyDown, Quit

from ..esper_ext import Processor, WorldExt
from ..resources.input_action import (InputAction, move_east, move_north,
                                      move_south, move_west, quit)


class EventDispatchStrategy(EventDispatch):
    def __init__(self, world: WorldExt):
        self.world = world


class SimpleDispatch(EventDispatchStrategy):
    key_to_action: ClassVar[Dict[int, InputAction]] = {
        tcod.event.K_UP: move_north,
        tcod.event.K_RIGHT: move_east,
        tcod.event.K_DOWN: move_south,
        tcod.event.K_LEFT: move_west,
        tcod.event.K_ESCAPE: quit,
    }

    def _set_input_action(self, action: InputAction) -> None:
        self.world.add_resource(action)

    def ev_quit(self, event: Quit) -> None:
        self._set_input_action(quit)

    def ev_keydown(self, event: KeyDown) -> None:
        self._set_input_action(self.key_to_action[event.sym])


class InputProcessor(Processor):
    def __init__(self):
        self.dispatch: Optional[EventDispatchStrategy] = None

    def get_dispatch(self) -> EventDispatchStrategy:
        if not self.dispatch or self.dispatch.world is not self.world:
            self.dispatch = SimpleDispatch(self.world)
        return self.dispatch

    def process(self):
        dispatch = self.get_dispatch()
        for event in tcod.event.get():
            dispatch.dispatch(event)
