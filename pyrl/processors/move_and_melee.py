#!/usr/bin/env python

from pyrl.components import Collider, Energy, Fighter, Name, Player, Position, Velocity
from pyrl.components.action import Action, MoveOrMelee
from pyrl.resources import Messages
from pyrl.world_helpers import ActionProcessor, act, defense, power


class MoveAndMeleeProcessor(ActionProcessor):
    @act(MoveOrMelee)
    def process_action(self, ent: int, action: MoveOrMelee, energy: Energy):
        self.world.add_component(ent, energy.consume(action.energy_cost))

        messages = self.world.get_resource(Messages)

        position = self.world.component_for_entity(ent, Position)
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

            damage = power(self.world, ent) - defense(self.world, target_entity)

            if damage > 0:
                self.world.add_component(
                    target_entity, target_fighter.take_damage(damage),
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
            # print(f"{self.world.component_for_entity(ent, Name)} {ent} moves")

        self.world.remove_component(ent, Action)
