#!/usr/bin/env python
import tcod

from pyrl.components import Energy, Fighter, Position, Stairs
from pyrl.components.action import Action, SimpleAction, take_stairs
from pyrl.mapgen import generate_level
from pyrl.resources import Map, Messages
from pyrl.world_helpers import ActionProcessor, act, only_player


class StairsProcessor(ActionProcessor):
    @act(take_stairs)
    @only_player
    def process_action(self, ent: int, action: SimpleAction, energy: Energy) -> None:
        actor_position = self.world.component_for_entity(ent, Position)
        messages = self.world.get_resource(Messages)

        for _, (stairs_position, stairs) in self.world.get_components(Position, Stairs):
            if stairs_position == actor_position:
                break
        else:
            messages.append("There are no stairs here.", tcod.yellow)
            self.world.remove_component(ent, Action)
            return

        self.world.add_component(ent, energy.consume(action.energy_cost))
        self.world.remove_component(ent, Action)
        messages.append(
            "You take a moment to rest, and recover your strength.", tcod.light_violet
        )
        fighter = self.world.component_for_entity(ent, Fighter)
        self.world.add_component(ent, fighter.heal(fighter.max_hp // 2))

        for cleanup, _ in self.world.get_component(Position):
            if cleanup is not ent:
                self.world.delete_entity(cleanup)

        generate_level(self.world, stairs.to_level)
        self.world.add_component(ent, self.world.get_resource(Map).spawn_position)
