#!/usr/bin/env python
import tcod

from pyrl.components import Fighter, Player, Visual
from pyrl.components.visual import RenderOrder
from pyrl.resources import Messages

from ..esper_ext import Processor


class PlayerDeathProcessor(Processor):
    def process(self, *args, **kwargs):
        messages = self.world.get_resource(Messages)
        for ent, (fighter, player) in self.world.get_components(Fighter, Player):
            if fighter.hp > 0:
                continue
            messages.append("You died!", tcod.red)
            self.world.add_component(
                ent, Visual("%", tcod.dark_red, RenderOrder.Corpse)
            )
