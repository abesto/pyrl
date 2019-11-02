#!/usr/bin/env python

from ..components import Collider, Energy, Name, Position
from ..components.action import Action, MoveOrMelee
from ..esper_ext import Processor


class MoveAndMeleeProcessor(Processor):
    def process(self):
        for ent, (position, action, energy) in self.world.get_components(
            Position, Action, Energy
        ):
            if not isinstance(action, MoveOrMelee):
                continue

            if not energy.consume(action.energy_cost):
                continue

            target_position = position + action.velocity
            for (
                blocker_entity,
                (name, blocker_position, _),
            ) in self.world.get_components(Name, Position, Collider):
                if blocker_position == target_position:
                    print(
                        f"You kick the {name.name} in the shin, much to its annoyance!"
                    )
                    break
            else:
                self.world.add_component(ent, action.velocity)
            self.world.remove_component(ent, Action)
