#!/usr/bin/env python
from pyrl.components import Collider
from pyrl.esper_ext import Processor

from ..components import Position, Velocity
from ..resources.map import Map


class CollisionProcessor(Processor):
    def process(self, *args, **kwargs):
        map = self.world.get_resource(Map)
        for ent, (position, velocity) in self.world.get_components(Position, Velocity):
            candidate_position = position.vector + velocity.vector

            collision = (
                (not 0 <= candidate_position.x < map.width)
                or (not 0 <= candidate_position.y < map.height)
                or map.tiles[candidate_position.x][candidate_position.y].blocked
            )

            if not collision:
                for _ent, (other_position, _collider) in self.world.get_components(
                    Position, Collider
                ):
                    if other_position == candidate_position:
                        collision = True
                        break

            if collision:
                self.world.remove_component(ent, Velocity)
