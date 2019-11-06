#!/usr/bin/env python
from pyrl.components import Energy, Name
from pyrl.components.action import Action, ponder
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class PonderProcessor(Processor):
    def process(self):
        for ent, (name, action, energy) in self.world.get_components(
            Name, Action, Energy
        ):
            if action is not ponder:
                continue
            messages = self.world.get_resource(Messages)
            if energy.can_act:
                messages.append(f"{name} ponders the meaning of existence")
                self.world.add_component(ent, energy.consume(action.energy_cost))
