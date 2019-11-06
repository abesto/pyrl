#!/usr/bin/env python

from ..components import Energy, Player
from ..esper_ext import Processor


class TimeProcessor(Processor):
    def __init__(self):
        self.turn = 0

    def process(self):
        # If the player has enough energy to act, stop ticking until they do
        for ent, (energy, _) in self.world.get_components(Energy, Player):
            if energy.can_act:
                return
        # Time passes
        for ent, energy in self.world.get_component(Energy):
            self.world.add_component(ent, energy.gain(1))
        # Debugging
        print(f"Turn {self.turn} is over")
        self.turn += 1
