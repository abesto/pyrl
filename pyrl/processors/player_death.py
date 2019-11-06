#!/usr/bin/env python
import tcod

from pyrl.components import Fighter, Player, Visual
from pyrl.resources import Messages

from ..esper_ext import Processor


class PlayerDeathProcessor(Processor):
    def process(self):
        messages = self.world.get_resource(Messages)
        for ent, (fighter, player) in self.world.get_components(Fighter, Player):
            if fighter.hp > 0:
                continue
            messages.append("You died!", tcod.red)
            self.world.remove_component(ent, Player)
            self.world.remove_component(ent, Fighter)
            self.world.add_component(ent, Visual("%", tcod.dark_red))
