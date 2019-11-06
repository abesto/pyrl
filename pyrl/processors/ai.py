#!/usr/bin/env python

import tcod

from pyrl.components import Collider, Player, Position
from pyrl.components.action import Action, MoveOrMelee, skip_one
from pyrl.components.ai import Ai
from pyrl.components.ai import Kind as AiKind
from pyrl.esper_ext import Processor
from pyrl.resources import Map, fov, input_action
from pyrl.vector import Vector


class AiProcessor(Processor):
    def process(self):
        for ent, ai in self.world.get_component(Ai):
            if ai.kind is AiKind.Player:
                self._process_player_ai(ent)
            elif ai.kind is AiKind.Basic:
                self._process_basic_ai(ent)
            else:
                raise NotImplementedError

    def _process_player_ai(self, ent: int) -> None:
        action = self.world.get_resource(input_action.InputAction)
        if isinstance(action, input_action.Move):
            self.world.add_component(
                ent,
                MoveOrMelee(
                    vector=action.vector, attack_monster=True, attack_player=False,
                ),
            )

    def _process_basic_ai(self, ent: int) -> None:
        player, (player_position, _) = self.world.get_components(Position, Player)[0]
        position = self.world.component_for_entity(ent, Position)
        fov_map = self.world.get_resource(fov.Fov).fov_map

        action: Action
        if fov_map.fov[position.y, position.x]:
            action = MoveOrMelee(
                vector=self._astar_step(position.vector, player_position.vector),
                attack_player=True,
                attack_monster=False,
            )
        else:
            action = skip_one

        self.world.add_component(ent, action)

    def _astar_step(self, src: Vector, dst: Vector) -> Vector:
        # Create a FOV map that has the dimensions of the map
        game_map = self.world.get_resource(Map)
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(
                    fov,
                    x1,
                    y1,
                    not game_map.tiles[x1][y1].block_sight,
                    not game_map.tiles[x1][y1].blocked,
                )

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for _, (position, _) in self.world.get_components(Position, Collider):
            if position.vector not in (src, dst):
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, position.x, position.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, src.x, src.y, dst.x, dst.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x and y:
                return (Vector(x, y) - src).norm()
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            return (dst - src).norm()

            # Delete the path to free memory
        tcod.path_delete(my_path)
