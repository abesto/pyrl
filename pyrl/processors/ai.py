#!/usr/bin/env python

from typing import ClassVar, Dict

from ..components import Name
from ..components.action import MoveOrMelee, ponder
from ..components.ai import Ai
from ..components.ai import Kind as AiKind
from ..components.velocity import Heading, Velocity
from ..esper_ext import Processor
from ..resources import input_action


class AiProcessor(Processor):
    input_action_to_heading: ClassVar[Dict[input_action.InputAction, Heading]] = {
        input_action.move_north: Heading.North,
        input_action.move_east: Heading.East,
        input_action.move_south: Heading.South,
        input_action.move_west: Heading.West,
    }

    def process(self):
        for ent, ai in self.world.get_component(Ai):
            if ai.kind is AiKind.Player:
                self._process_player_ai(ent)
            elif ai.kind is AiKind.Basic:
                self._process_basic_ai(ent)
            else:
                raise NotImplementedError

    def _process_player_ai(self, ent: int) -> None:
        action = self.world.get_resource(input_action.InputAction)
        if action in (
            input_action.move_north,
            input_action.move_east,
            input_action.move_south,
            input_action.move_west,
        ):
            self.world.add_component(
                ent,
                MoveOrMelee(
                    velocity=Velocity(
                        heading=self.input_action_to_heading[action], magnitude=1
                    ),
                    attack_monster=True,
                    attack_player=False,
                ),
            )
            self.world.add_resource(input_action.noop)

    def _process_basic_ai(self, ent: int) -> None:
        self.world.add_component(ent, ponder)
