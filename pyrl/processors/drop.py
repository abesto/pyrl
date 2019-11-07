#!/usr/bin/env python
import tcod

from pyrl.components import Energy, Inventory, Name, Position
from pyrl.components.action import Action, DropFromInventory
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class DropProcessor(Processor):
    def process(self, ent: int):
        action = self.world.try_component(ent, Action)
        if not isinstance(action, DropFromInventory):
            return

        energy = self.world.component_for_entity(ent, Energy)
        if not energy.can_act:
            return

        inventory = self.world.component_for_entity(ent, Inventory)
        item_ent = inventory.items[action.index]
        name = self.world.component_for_entity(item_ent, Name)

        self.world.add_component(ent, inventory.remove_item_at(action.index))
        self.world.add_component(
            item_ent, self.world.component_for_entity(ent, Position)
        )
        self.world.get_resource(Messages).append(f"You dropped the {name}", tcod.yellow)

        self.world.remove_component(ent, Action)
