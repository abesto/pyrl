#!/usr/bin/env python
import tcod

from pyrl.components import (
    Collider,
    Energy,
    Fighter,
    Level,
    Name,
    Player,
    Visual,
    XpReward,
)
from pyrl.components.action import Action
from pyrl.components.ai import Ai
from pyrl.components.visual import RenderOrder
from pyrl.esper_ext import Processor
from pyrl.resources import Messages
from pyrl.world_helpers import ProcessorExt


class MonsterDeathProcessor(ProcessorExt):
    def process(self, *args, **kwargs):
        messages = self.world.get_resource(Messages)
        for ent, (name, fighter) in self.world.get_components(Name, Fighter):
            if self.world.has_component(ent, Player):
                continue
            if fighter.alive:
                continue

            messages.append(f"{str(name).capitalize()} is dead!", tcod.orange)
            for component in (Fighter, Ai, Collider, Action, Energy):
                if self.world.has_component(ent, component):
                    self.world.remove_component(ent, component)
            self.world.add_component(
                ent, Visual("%", tcod.dark_red, RenderOrder.CORPSE)
            )
            self.world.add_component(ent, Name(f"remains of {name}"))

            player = self.player
            if not player:
                return

            xp = self.world.component_for_entity(ent, XpReward).amount
            self.world.add_component(
                player, self.world.component_for_entity(player, Level).add_xp(xp)
            )
            self.world.get_resource(Messages).append(
                f"You gain {xp} experience points."
            )
