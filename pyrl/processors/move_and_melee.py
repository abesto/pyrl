#!/usr/bin/env python

from ..components import Position
from ..components.action import Action, MoveOrMelee
from ..esper_ext import Processor


class MoveAndMeleeProcessor(Processor):
    def process(self):
        for ent, (position, action) in self.world.get_components(Position, Action):
            if not isinstance(action, MoveOrMelee):
                continue
            # TODO melee code will go here
            self.world.add_component(ent, action.velocity)
            self.world.remove_component(ent, Action)
