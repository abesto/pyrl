#!/usr/bin/env python
from pyrl.world_helpers import ActionProcessor, act

from ..components import Energy
from ..components.action import Action, Skip


class SkipProcessor(ActionProcessor):
    @act(Skip)
    def process_action(self, ent: int, action: Skip, energy: Energy):
        self.world.add_component(ent, energy.consume(action.energy_cost))
        self.world.remove_component(ent, Action)
