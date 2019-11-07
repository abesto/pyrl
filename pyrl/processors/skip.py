#!/usr/bin/env python

from ..components import Energy
from ..components.action import Action, Skip
from ..esper_ext import Processor


class SkipProcessor(Processor):
    def process(self, ent: int):
        action = self.world.try_component(ent, Action)
        if not isinstance(action, Skip):
            return

        energy = self.world.component_for_entity(ent, Energy)
        if not energy.can_act:
            return

        self.world.add_component(ent, energy.consume(action.energy_cost))
        self.world.remove_component(ent, Action)
