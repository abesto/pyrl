#!/usr/bin/env python

from dataclasses import replace

from pyrl.components import Collider, Energy, Fighter, Name, Player, Position, Velocity
from pyrl.components.action import Action, MoveOrMelee
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class MoveAndMeleeProcessor(Processor):
    def process(self, ent: int):
        action = self.world.try_component(ent, Action)
        if not isinstance(action, MoveOrMelee):
            return

        energy = self.world.component_for_entity(ent, Energy)
        if not energy.can_act:
            return

        self.world.add_component(ent, energy.consume(action.energy_cost))

        messages = self.world.get_resource(Messages)

        position = self.world.component_for_entity(ent, Position)
        fighter = self.world.component_for_entity(ent, Fighter)
        target_vector = position.vector + action.vector
        for (
            target_entity,
            (target_position, target_fighter, _),
        ) in self.world.get_components(Position, Fighter, Collider):
            if target_position.vector != target_vector:
                continue

            player_is_target = self.world.has_component(target_entity, Player)
            attacker_name = str(self.world.component_for_entity(ent, Name)).capitalize()
            target_name = str(self.world.component_for_entity(target_entity, Name))

            if (player_is_target and not action.attack_player) or (
                not player_is_target and not action.attack_monster
            ):
                messages.append(
                    f"{attacker_name} stops just short of attacking {target_name}"
                )
                break

            damage = fighter.power - target_fighter.defense

            if damage > 0:
                self.world.add_component(
                    target_entity,
                    replace(target_fighter, hp=target_fighter.hp - damage),
                )
                messages.append(
                    f"{attacker_name} attacks {target_name} for {damage} hit points"
                )
            else:
                messages.append(
                    f"{attacker_name} attacks {target_name} but does no damage"
                )
            break
        else:
            self.world.add_component(ent, Velocity(action.vector))
            print(f"{self.world.component_for_entity(ent, Name)} {ent} moves")

        self.world.remove_component(ent, Action)
