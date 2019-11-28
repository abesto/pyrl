#!/usr/bin/env python
from pyrl.components import Fighter

from ..components import Energy, Player
from ..esper_ext import Processor


class TimeProcessor(Processor):
    def process(self):
        # If the player has enough energy to act, stop ticking until they do
        for ent, (energy, _) in self.world.get_components(Energy, Player):
            if energy.can_act:
                return

        # Time passes
        for ent, energy in self.world.get_component(Energy):
            self.world.add_component(ent, energy.gain(1))
