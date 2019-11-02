#!/usr/bin/env python

import tcod.console

from .. import config
from ..components import Position, Visual
from ..esper_ext import Processor
from ..resources import Fov
from ..resources.map import Map


class RenderProcessor(Processor):
    def process(self):
        root = self.world.get_resource(tcod.console.Console)
        buffer = tcod.console.Console(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self._process_map(buffer)
        self._process_entities(buffer)
        buffer.blit(root, width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        tcod.console_flush()

    def _process_entities(self, buffer: tcod.console.Console) -> None:
        fov_map = self.world.get_resource(Fov).fov_map
        for ent, (position, visual) in self.world.get_components(Position, Visual):
            if not fov_map.fov[position.y, position.x]:
                continue
            buffer.print(position.x, position.y, visual.char, fg=visual.color)

    def _process_map(self, buffer: tcod.console.Console) -> None:
        map = self.world.get_resource(Map)
        fov_map = self.world.get_resource(Fov).fov_map
        for x, column in enumerate(map.tiles):
            for y, tile in enumerate(column):
                if not tile.explored:
                    continue
                wall = tile.block_sight
                visible = fov_map.fov[y, x]

                if wall:
                    char = "#"
                else:
                    char = "."

                buffer.print(
                    x, y, char, bg=config.theme.background_color(wall, visible)
                )
