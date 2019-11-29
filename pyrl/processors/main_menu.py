#!/usr/bin/env python

from pyrl import saveload
from pyrl.esper_ext import Processor
from pyrl.mapgen import add_player, generate_level
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
        generate_level(self.world)
        add_player(self.world)
        self.world.add_resource(Messages(5))

    def _load(self) -> None:
        if saveload.load(self.world):
            self.world.add_resource(Fov(self.world.get_resource(Map)))
        else:
            self.world.add_resource(main_menu)

    def _save(self) -> None:
        saveload.save(self.world)
