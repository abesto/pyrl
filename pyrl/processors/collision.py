#!/usr/bin/env python

from ..components import Position, Velocity
from ..esper_ext import Processor
from ..resources.map import Map


class CollisionProcessor(Processor):
    def process(self):
        map = self.world.get_resource(Map)
        for ent, (position, velocity) in self.world.get_components(Position, Velocity):
            candidate_position = position + velocity
            if map.tiles[candidate_position.x][candidate_position.y].blocked:
                self.world.remove_component(ent, Velocity)
