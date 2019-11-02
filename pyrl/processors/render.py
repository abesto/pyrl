#!/usr/bin/env python

import tcod.console

from .. import config
from ..components import Position, Visual
from ..esper_ext import Processor


class RenderProcessor(Processor):
    def process(self):
        root = self.world.get_resource(tcod.console.Console)
        buffer = tcod.console.Console(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        for ent, (position, visual) in self.world.get_components(Position, Visual):
            buffer.put_char(
                position.x + 1, position.y + 1, ord(visual.char), tcod.BKGND_NONE
            )
        buffer.blit(root, width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        tcod.console_flush()
