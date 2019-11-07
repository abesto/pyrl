#!/usr/bin/env python

from ..components import Position, Velocity
from ..esper_ext import Processor
from ..resources.map import Map


class CollisionProcessor(Processor):
    def process(self, *args, **kwargs):
        map = self.world.get_resource(Map)
        for ent, (position, velocity) in self.world.get_components(Position, Velocity):
            candidate_position = position.vector + velocity.vector
            if (
                (not 0 <= candidate_position.x < map.width)
                or (not 0 <= candidate_position.y < map.height)
                or map.tiles[candidate_position.x][candidate_position.y].blocked
            ):
                self.world.remove_component(ent, Velocity)
