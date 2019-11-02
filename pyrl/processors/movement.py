#!/usr/bin/env python
from ..components import Player, Position, Velocity
from ..esper_ext import Processor
from ..resources import Fov


class MovementProcessor(Processor):
    def process(self):
        for ent, (position, velocity,) in self.world.get_components(Position, Velocity):
            position += velocity
            velocity.magnitude = 0
            if self.world.has_component(ent, Player):
                self.world.get_resource(Fov).should_recompute = True
