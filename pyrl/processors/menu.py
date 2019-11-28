#!/usr/bin/env python
from pyrl import config
from pyrl.components import Inventory, Name, Player
from pyrl.esper_ext import Processor
from pyrl.resources import Menu
from pyrl.resources.input_action import (
    DropFromInventory,
    InputAction,
    MenuChoice,
    UseFromInventory,
    dismiss_menu,
    load,
    new_game,
    noop,
    open_drop_menu,
    open_inventory,
    quit,
)
from pyrl.resources.menu import MenuType


class MenuProcessor(Processor):
    def process(self):
        input_action = self.world.get_resource(InputAction)

        if input_action is open_inventory:
            for _, (_, inventory) in self.world.get_components(Player, Inventory):
                names = [
                    self.world.component_for_entity(item, Name).name
                    for item in inventory.items
                ]
                self.world.add_resource(
                    Menu(
                        MenuType.INVENTORY,
                        "Press the key next to an item to use it, or Esc to cancel.\n",
                        names,
                        config.INVENTORY_WIDTH,
                    )
                )
            self.world.add_resource(noop)

        elif input_action is open_drop_menu:
            for _, (_, inventory) in self.world.get_components(Player, Inventory):
                names = [
                    self.world.component_for_entity(item, Name).name
                    for item in inventory.items
                ]
                self.world.add_resource(
                    Menu(
                        MenuType.DROP,
                        "Press the key next to an item to drop it, or Esc to cancel.\n",
                        names,
                        config.INVENTORY_WIDTH,
                    )
                )
            self.world.add_resource(noop)

        elif (
            input_action is dismiss_menu
            and self.world.get_resource(Menu).menu_type is not MenuType.MAIN
        ):
            self.world.remove_resource(Menu)
            self.world.add_resource(noop)

        elif isinstance(input_action, MenuChoice):
            menu = self.world.get_resource(Menu)

            if input_action.choice >= len(menu.options):
                self.world.add_resource(noop)

            elif menu.menu_type is MenuType.INVENTORY:
                self.world.add_resource(UseFromInventory(input_action.choice))
                self.world.remove_resource(Menu)

            elif menu.menu_type is MenuType.DROP:
                self.world.add_resource(DropFromInventory(input_action.choice))
                self.world.remove_resource(Menu)

            elif menu.menu_type is MenuType.MAIN:
                new_action = {0: new_game, 1: load, 2: quit}.get(
                    input_action.choice, noop
                )
                self.world.add_resource(new_action)
                if new_action is not noop:
                    self.world.remove_resource(Menu)

            else:
                raise NotImplementedError()
