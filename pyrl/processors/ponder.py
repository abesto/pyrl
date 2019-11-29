#!/usr/bin/env python
from pyrl.components import Energy, Name
from pyrl.components.action import SimpleAction, ponder
from pyrl.resources import Messages
from pyrl.world_helpers import ActionProcessor, act


class PonderProcessor(ActionProcessor):
    @act(ponder)
    def process_action(self, ent: int, action: SimpleAction, energy: Energy):
        name = self.world.component_for_entity(ent, Name)
        messages = self.world.get_resource(Messages)
        messages.append(f"{name} ponders the meaning of existence")
        self.world.add_component(ent, energy.consume(action.energy_cost))
