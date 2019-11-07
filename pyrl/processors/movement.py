#!/usr/bin/env python
from ..components import Player, Position, Velocity
from ..esper_ext import Processor
from ..resources import Fov


class MovementProcessor(Processor):
    def process(self, ent: int):
        if not self.world.has_component(ent, Velocity):
            return
        position, velocity = [
            self.world.component_for_entity(ent, c) for c in (Position, Velocity)
        ]
        self.world.add_component(ent, position + velocity)
        self.world.remove_component(ent, Velocity)
        if self.world.has_component(ent, Player):
            self.world.get_resource(Fov).should_recompute = True
