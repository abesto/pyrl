#!/usr/bin/env python
import tcod

from pyrl.components import Energy, Inventory, Name, Position
from pyrl.components.action import Action, pickup
from pyrl.components.inventory import InventoryFullException
from pyrl.components.item import Item
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class PickupProcessor(Processor):
    def process(self, actor_ent: int):
        action = self.world.try_component(actor_ent, Action)
        if action is not pickup:
            return

        energy = self.world.component_for_entity(actor_ent, Energy)
        if not energy.can_act:
            return

        messages = self.world.get_resource(Messages)
        actor_position = self.world.component_for_entity(actor_ent, Position)
        for item_ent, (item_position, _) in self.world.get_components(Position, Item):
            if actor_position != item_position:
                continue

            inventory = self.world.component_for_entity(actor_ent, Inventory)
            try:
                inventory = inventory.add(item_ent)
            except InventoryFullException:
                messages.append("You cannot carry any more, your inventory is full")
                break
            else:
                self.world.add_component(actor_ent, inventory)
                self.world.remove_component(item_ent, Position)
                name = self.world.component_for_entity(item_ent, Name)
                messages.append(f"You picked up the {name}!", tcod.blue)
                self.world.add_component(actor_ent, energy.consume(action.energy_cost))
                break
        else:
            messages.append("There is nothing here to pick up.")

        self.world.remove_component(actor_ent, Action)
