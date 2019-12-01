#!/usr/bin/env python
from pyrl.world_helpers import ProcessorExt

from .. import config
from ..components import Position
from ..resources import Fov, Map


class FovProcessor(ProcessorExt):
    def process(self):
        fov = self.world.try_resource(Fov)
        if fov is None:
            return
        if not fov.should_recompute:
            return

        player = self.player
        if not player:
            return

        player_position = self.world.component_for_entity(player, Position)

        # Compute the FOV
        fov.fov_map.compute_fov(
            x=player_position.x,
            y=player_position.y,
            radius=config.FOV_RADIUS,
            light_walls=config.FOV_LIGHT_WALLS,
            algorithm=config.FOV_ALGORITHM,
        )

        # Book-keeping
        fov.should_recompute = False

        # Update "explored" records
        map = self.world.get_resource(Map)
        for x in range(map.width):
            for y in range(map.height):
                if fov.fov_map.fov[y, x]:
                    map.tiles[x][y].explored = True
