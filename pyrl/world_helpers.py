#!/usr/bin/env python3
from typing import Iterable, Optional

from pyrl.components import Energy, Player
from pyrl.components.action import Action
from pyrl.esper_ext import Processor, WorldExt
from pyrl.resources.input_action import InputAction, noop, quit


def gen_next_actor(world: WorldExt) -> Iterable[int]:
    # First: if the player can move, then they should
    for ent, (_, energy) in world.get_components(Player, Energy):
        if energy.can_act:
            yield ent
    # Then, everyone else can act
    for ent, (energy,) in world.get_components(Energy):
        if energy.can_act:
            yield ent


class RunPerActor(Processor):
    _world: WorldExt

    def __init__(self, *children: Processor):
        self.children = children

    def _run_children(self, ent: int) -> None:
        for child in self.children:
            # print(f"  {type(child)}")
            child.process(ent)

    def process(self, *args, **kwargs) -> None:
        for next_actor in gen_next_actor(self.world):
            if self.world.has_component(next_actor, Player):
                have_input = self.world.try_resource(InputAction) not in (noop, quit)
                have_player_action = bool(self.world.get_components(Action, Player))
                if not (have_input or have_player_action):
                    return
            self._run_children(next_actor)

    @property
    def world(self) -> WorldExt:
        return self._world

    @world.setter
    def world(self, value: WorldExt) -> None:
        self._world = value
        for child in self.children:
            child.world = value
