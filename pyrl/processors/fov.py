#!/usr/bin/env python

from .. import config
from ..components import Player, Position
from ..esper_ext import Processor
from ..resources import Fov, Map


class FovProcessor(Processor):
    def process(self):
        fov = self.world.try_resource(Fov)
        if fov is None:
            return
        if fov.should_recompute:
            # Grab the player position. For FOV calculation, we require a single player entity
            players = self.world.get_components(Player, Position)
            if not players:
                return
            if len(players) > 1:
                raise Exception(
                    "More than 1 entity found with Player flag component, what gives?"
                )
            player_position = players[0][1][1]

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
