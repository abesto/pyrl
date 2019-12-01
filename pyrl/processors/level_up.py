#!/usr/bin/env python
from dataclasses import replace

import tcod

from pyrl.components import Fighter, Level
from pyrl.resources import Menu, Messages
from pyrl.resources.input_action import InputAction, LevelUpChoice, noop
from pyrl.resources.menu import MenuType
from pyrl.world_helpers import ProcessorExt


class LevelUpProcessor(ProcessorExt):
    def process(self, *args, **kwargs):
        self._trigger_level_up()
        self._handle_level_up_choice()

    def _trigger_level_up(self) -> None:
        if self.world.try_resource(Menu) is not None:
            return

        player = self.player
        if not player:
            return

        next_level = self.world.component_for_entity(player, Level).level_up()
        if not next_level:
            return

        self.world.get_resource(Messages).append(
            f"Your battle skills grow stronger! You reached level {next_level.current_level}!",
            tcod.yellow,
        )
        self.world.add_component(player, next_level)

        fighter = self.world.component_for_entity(player, Fighter)
        self.world.add_resource(
            Menu(
                menu_type=MenuType.LEVEL_UP,
                header="Level up! Choose a stat to raise:",
                width=40,
                options=[
                    f"Constitution (+20 HP, from {fighter.max_hp})",
                    f"Strength (+1 attack, from {fighter.power})",
                    f"Agility (+1 defense, from {fighter.defense})",
                ],
            )
        )

    def _handle_level_up_choice(self) -> None:
        choice = self.world.try_resource(InputAction)
        if not isinstance(choice, LevelUpChoice):
            return

        player = self.player
        if not player:
            return

        fighter = self.world.component_for_entity(player, Fighter)
        if choice is LevelUpChoice.HP:
            self.world.add_component(
                player, replace(fighter, hp=fighter.hp + 20, max_hp=fighter.max_hp + 20)
            )
        elif choice is LevelUpChoice.DEF:
            self.world.add_component(
                player, replace(fighter, defense=fighter.defense + 1)
            )
        elif choice is LevelUpChoice.STR:
            self.world.add_component(player, replace(fighter, power=fighter.power + 1))

        self.world.remove_resource(Menu)
        self.world.add_resource(noop)
