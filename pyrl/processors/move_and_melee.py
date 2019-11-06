#!/usr/bin/env python

from typing import cast

from ..components import Collider, Energy, Name, Player, Position, Velocity
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

            target_vector = position.vector + action.vector
            for (blocker_entity, (blocker_position, _),) in self.world.get_components(
                Position, Collider
            ):
                if blocker_position.vector != target_vector:
                    continue

                player_is_target = self.world.has_component(blocker_entity, Player)
                player_is_attacker = self.world.has_component(ent, Player)

                attacker_name = (
                    "You"
                    if player_is_attacker
                    else self.world.component_for_entity(ent, Name)
                )
                target_name = (
                    "you"
                    if player_is_target
                    else self.world.component_for_entity(blocker_entity, Name)
                )

                if (player_is_target and action.attack_player) or (
                    not player_is_target and action.attack_monster
                ):
                    print(f"{attacker_name} kicks {target_name}! Drama!")

                break
            else:
                self.world.add_component(ent, Velocity(action.vector))
                print(f"{self.world.component_for_entity(ent, Name)} {ent} moves")

            self.world.remove_component(ent, Action)
            break
