#!/usr/bin/env python
import tcod

from pyrl.components import Collider, Energy, Fighter, Name, Player, Visual
from pyrl.components.action import Action
from pyrl.components.ai import Ai
from pyrl.components.visual import RenderOrder
from pyrl.esper_ext import Processor
from pyrl.resources import Messages


class MonsterDeathProcessor(Processor):
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
