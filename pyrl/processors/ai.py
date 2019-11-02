#!/usr/bin/env python

from typing import ClassVar, Dict

from ..components import Velocity
from ..components.ai import Ai
from ..components.ai import Kind as AiKind
from ..components.velocity import Heading
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
            else:
                raise NotImplementedError
        self.world.add_resource(input_action.noop)

    def _process_player_ai(self, ent: int):
        action = self.world.get_resource(input_action.InputAction)
        if action in (
            input_action.move_north,
            input_action.move_east,
            input_action.move_south,
            input_action.move_west,
        ):
            self.world.add_component(
                ent, Velocity(heading=self.input_action_to_heading[action], magnitude=1)
            )
