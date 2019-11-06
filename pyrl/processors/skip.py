#!/usr/bin/env python

from ..components import Energy
from ..components.action import Action, Skip
from ..esper_ext import Processor


class SkipProcessor(Processor):
    def process(self):
        for _, (action, energy) in self.world.get_components(Action, Energy):
            if not isinstance(action, Skip):
                continue
            energy.consume(action.energy_cost)
