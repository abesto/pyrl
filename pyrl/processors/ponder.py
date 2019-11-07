#!/usr/bin/env python
from pyrl.components import Energy, Name
from pyrl.components.action import Action, ponder
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class PonderProcessor(Processor):
    def process(self, ent: int):
        action = self.world.try_component(ent, Action)
        if action is not ponder:
            return

        energy = self.world.component_for_entity(ent, Energy)
        if not energy.can_act:
            return

        name = self.world.component_for_entity(ent, Name)
        messages = self.world.get_resource(Messages)
        messages.append(f"{name} ponders the meaning of existence")
        self.world.add_component(ent, energy.consume(action.energy_cost))
