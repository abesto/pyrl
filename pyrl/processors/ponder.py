#!/usr/bin/env python
from pyrl.components import Energy, Name
from pyrl.components.action import Action, ponder

from ..esper_ext import Processor


class PonderProcessor(Processor):
    def process(self):
        for _, (name, action, energy) in self.world.get_components(
            Name, Action, Energy
        ):
            if action is not ponder:
                continue
            elif energy.consume(action.energy_cost):
                print(f"{name} ponders the meaning of existence")
