#!/usr/bin/env python

from ..components import Position, Velocity
from ..esper_ext import Processor


class MovementProcessor(Processor):
    def process(self):
        for ent, (position, velocity,) in self.world.get_components(Position, Velocity):
            position += velocity
            velocity.magnitude = 0
