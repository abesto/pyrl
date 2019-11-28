#!/usr/bin/env python
import tcod

from pyrl.components import Collider, Energy, Fighter, Player, Visual
from pyrl.components.action import Action
from pyrl.components.ai import Ai
from pyrl.components.visual import RenderOrder
from pyrl.resources import Messages

from ..esper_ext import Processor


class PlayerDeathProcessor(Processor):
    def process(self, *args, **kwargs):
        messages = self.world.get_resource(Messages)
        for ent, (fighter, player) in self.world.get_components(Fighter, Player):
            if fighter.alive:
                continue
            print("player died")
            messages.append("You died!", tcod.red)
            self.world.add_component(
                ent, Visual("%", tcod.dark_red, RenderOrder.Corpse)
            )
            for component in (Ai, Fighter, Collider, Action, Energy):
                try:
                    self.world.remove_component(ent, component)
                except KeyError:
                    pass
