#!/usr/bin/env python
import tcod

from pyrl.components import (
    Energy,
    Equipment,
    Equippable,
    Fighter,
    Inventory,
    Name,
    Player,
    Position,
)
from pyrl.components.action import Action, UseFromInventory
from pyrl.components.ai import Ai, ConfusedAi
from pyrl.components.item import Item
from pyrl.resources import Fov, Messages
from pyrl.world_helpers import ActionProcessor, act


class UseItemProcessor(ActionProcessor):
    @act(UseFromInventory)
    def process_action(
        self, actor: int, action: UseFromInventory, energy: Energy
    ) -> None:
        inventory = self.world.component_for_entity(actor, Inventory)
        item_ent = inventory.items[action.index]
        item = self.world.try_component(item_ent, Item)
        messages = self.world.get_resource(Messages)

        if self.world.try_component(item_ent, Equippable):
            equipment = self.world.component_for_entity(actor, Equipment).toggle_equip(
                self.world, item_ent
            )
            self.world.add_component(actor, equipment)
            name = self.world.component_for_entity(item_ent, Name)
            if equipment.is_equipped(item_ent):
                messages.append(f"You equipped the {name}")
            else:
                messages.append(f"You unequipped the {name}")
            self.world.add_component(actor, energy.consume(action.energy_cost))

        # This could be refactored into "effects" (+ "perception") systems

        elif item is Item.HEALING_POTION:
            fighter = self.world.component_for_entity(actor, Fighter)
            if fighter.hp >= fighter.max_hp:
                messages.append("You are already at full health", tcod.yellow)
            else:
                messages.append("Your wounds start to feel better!", tcod.green)
                self.world.add_component(actor, fighter.heal(40))
                self.world.add_component(actor, energy.consume(action.energy_cost))
                self.world.add_component(actor, inventory.remove_item_at(action.index))
                self.world.delete_entity(item_ent)

        elif item is Item.LIGHTNING_SCROLL:
            damage = 40
            maximum_range = 5
            fov_map = self.world.get_resource(Fov).fov_map
            actor_position = self.world.component_for_entity(actor, Position)

            closest_distance, target = maximum_range + 1, None
            for candidate, (candidate_position, _) in self.world.get_components(
                Position, Fighter
            ):
                if self.world.has_component(actor, Player) == self.world.has_component(
                    candidate, Player
                ):
                    continue
                if not fov_map.fov[candidate_position.y, candidate_position.x]:
                    continue

                distance = (candidate_position.vector - actor_position.vector).length
                if distance < closest_distance:
                    closest_distance, target = distance, candidate

            if target is None:
                messages.append("No enemy is close enough to strike.", tcod.red)
            else:
                name, fighter = [
                    self.world.component_for_entity(target, c) for c in [Name, Fighter]
                ]
                messages.append(
                    f"A lightning bolt strikes the {name} for {damage} damage!",
                )
                self.world.add_component(target, fighter.take_damage(damage))
                self.world.add_component(actor, inventory.remove_item_at(action.index))
                self.world.add_component(actor, energy.consume(action.energy_cost))
                self.world.delete_entity(item_ent)

        elif item is Item.FIREBALL_SCROLL:
            fov_map = self.world.get_resource(Fov).fov_map
            damage = 25
            radius = 3
            target = action.target

            if target is None:
                raise Exception(
                    "Target should be set for using a scroll of fireball, something went wrong :("
                )

            if not fov_map.fov[target.y, target.x]:
                messages.append(
                    "You cannot target a tile outside your field of view.", tcod.yellow
                )
            else:
                messages.append(
                    f"The fireball explodes, burning everything within {radius} tiles!",
                    tcod.orange,
                )
                for candidate, (position, fighter, name) in self.world.get_components(
                    Position, Fighter, Name
                ):
                    if (position.vector - target).length <= radius:
                        messages.append(
                            f"The {name} gets burned for {damage} hit points.",
                            tcod.orange,
                        )
                        self.world.add_component(candidate, fighter.take_damage(damage))
                self.world.add_component(actor, inventory.remove_item_at(action.index))
                self.world.add_component(actor, energy.consume(action.energy_cost))
                self.world.delete_entity(item_ent)

        elif item is Item.CONFUSION_SCROLL:
            fov_map = self.world.get_resource(Fov).fov_map
            target = action.target

            if target is None:
                raise Exception(
                    "Target should be set for using a scroll of confusion, something went wrong :("
                )

            if not fov_map.fov[target.y, target.x]:
                messages.append(
                    "You cannot target a tile outside your field of view.", tcod.yellow
                )
            else:
                for ent, (position, name, ai) in self.world.get_components(
                    Position, Name, Ai
                ):
                    if position.vector == target:
                        self.world.add_component(ent, ConfusedAi.new(ai, 10))
                        self.world.get_resource(Messages).append(
                            f"The eyes of the {name} look vacant, as he starts to stumble around!",
                            tcod.light_green,
                        )
                        self.world.add_component(
                            actor, inventory.remove_item_at(action.index)
                        )
                        self.world.add_component(
                            actor, energy.consume(action.energy_cost)
                        )
                        self.world.delete_entity(item_ent)
                        break
                else:
                    self.world.get_resource(Messages).append(
                        "There is no targetable enemy at that location.", tcod.yellow
                    )

        else:
            name = self.world.component_for_entity(item_ent, Name)
            messages.append(f"The {name} cannot be used")

        self.world.remove_component(actor, Action)
