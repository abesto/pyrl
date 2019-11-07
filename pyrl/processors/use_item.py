#!/usr/bin/env python
import tcod

from pyrl.components import Energy, Fighter, Inventory, Name
from pyrl.components.action import Action, UseFromInventory
from pyrl.components.item import Item
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class UseItemProcessor(Processor):
    def process(self, ent: int) -> None:
        action = self.world.try_component(ent, Action)
        if not isinstance(action, UseFromInventory):
            return

        energy = self.world.component_for_entity(ent, Energy)
        if not energy.can_act:
            return

        inventory = self.world.component_for_entity(ent, Inventory)
        item_ent = inventory.items[action.index]
        item = self.world.component_for_entity(item_ent, Item)

        # This could be refactored into "effects" + "perception" systems
        messages = self.world.get_resource(Messages)
        if item is Item.HEALING_POTION:
            fighter = self.world.component_for_entity(ent, Fighter)
            if fighter.hp >= fighter.max_hp:
                messages.append("You are already at full health", tcod.yellow)
            else:
                messages.append("Your wounds start to feel better!", tcod.green)
                self.world.add_component(ent, fighter.heal(4))
                self.world.add_component(ent, inventory.remove_item_at(action.index))
                self.world.add_component(ent, energy.consume(action.energy_cost))
        else:
            name = self.world.component_for_entity(item_ent, Name)
            messages.append(f"The {name} cannot be used")

        self.world.remove_component(ent, Action)
