#!/usr/bin/env python
from ..components import Player, Position, Velocity
from ..esper_ext import Processor
from ..resources import Fov


class MovementProcessor(Processor):
    def process(self):
        for ent, (position, velocity) in self.world.get_components(Position, Velocity):
            self.world.add_component(ent, position + velocity)
            self.world.remove_component(ent, Velocity)
            if self.world.has_component(ent, Player):
                self.world.get_resource(Fov).should_recompute = True
