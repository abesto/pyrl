#!/usr/bin/env python
import tcod

from pyrl import saveload
from pyrl.components import Collider, Energy, Fighter, Inventory, Name, Player, Visual
from pyrl.components.ai import player as player_ai
from pyrl.components.visual import RenderOrder
from pyrl.esper_ext import Processor
from pyrl.mapgen import generate_items, generate_monsters, random_map
from pyrl.resources import Fov, Map, Messages
from pyrl.resources.input_action import (
    InputAction,
    load,
    new_game,
    noop,
    quit_to_main_menu,
)
from pyrl.resources.menu import main_menu


class MainMenuProcessor(Processor):
    def process(self):
        input_action = self.world.get_resource(InputAction)

        if input_action is quit_to_main_menu:
            self._save()
            self._clear()
            self.world.add_resource(main_menu)
            self.world.add_resource(noop)

        elif input_action is new_game:
            self._clear()
            self._new()
            self.world.add_resource(noop)

        elif input_action is load:
            self._clear()
            self._load()
            self.world.add_resource(noop)

    def _clear(self) -> None:
        for resource_type in (Map, Fov, Messages):
            self.world.remove_resource(resource_type)
        self.world.clear_database()

    def _new(self) -> None:
        map = random_map()
        self.world.add_resource(map)
        self.world.add_resource(Fov(map))
        self.world.add_resource(Messages(5))

        self._add_player()
        generate_monsters(self.world)
        generate_items(self.world)

    def _add_player(self) -> None:
        map = self.world.get_resource(Map)
        self.world.create_entity(
            map.spawn_position,
            Visual("@", tcod.white, RenderOrder.Actor),
            player_ai,
            Player(),
            Name("Player"),
            Collider(),
            Energy(1),
            Fighter.new(hp=30, defense=2, power=5,),
            Inventory(26),
        )

    def _load(self) -> None:
        if saveload.load(self.world):
            self.world.add_resource(Fov(self.world.get_resource(Map)))
        else:
            self.world.add_resource(main_menu)

    def _save(self) -> None:
        saveload.save(self.world)
