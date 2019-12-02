#!/usr/bin/env python
from random import randint

import tcod

from pyrl.components import Collider, Inventory, Name, Player, Position
from pyrl.components.action import (
    Action,
    DropFromInventory,
    MoveOrMelee,
    UseFromInventory,
    pickup,
    skip_one,
    take_stairs,
)
from pyrl.components.ai import Ai, ConfusedAi
from pyrl.components.ai import Kind as AiKind
from pyrl.components.item import Item
from pyrl.resources import Map, Messages, Targeting, fov, input_action
from pyrl.vector import Vector
from pyrl.world_helpers import EntityProcessor


class AiProcessor(EntityProcessor):
    def process_entity(self, ent: int):
        ai = self.world.component_for_entity(ent, Ai)
        if ai.kind is AiKind.PLAYER:
            self._process_player_ai(ent)
        elif ai.kind is AiKind.BASIC:
            self._process_basic_ai(ent)
        elif ai.kind is AiKind.CONFUSED and isinstance(ai, ConfusedAi):
            self._process_confused_ai(ent, ai)
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
            self.world.add_resource(input_action.noop)

        elif action is input_action.pickup:
            self.world.add_component(ent, pickup)
            self.world.add_resource(input_action.noop)

        elif isinstance(action, input_action.UseFromInventory):
            item_ent = self.world.component_for_entity(ent, Inventory).items[
                action.index
            ]
            item = self.world.try_component(item_ent, Item)
            if item is not None and item.needs_targeting:
                target = action.target
                if target is None:
                    self.world.add_resource(
                        Targeting(
                            action.index,
                            item.targeting_radius,
                            self.world.component_for_entity(ent, Position).vector,
                        )
                    )
                else:
                    self.world.add_component(
                        ent, UseFromInventory(action.index, target)
                    )
            else:
                self.world.add_component(ent, UseFromInventory(action.index))
            self.world.add_resource(input_action.noop)

        elif action is input_action.cancel_targeting:
            self.world.remove_resource(Targeting)
            self.world.add_resource(input_action.noop)

        elif isinstance(action, input_action.DropFromInventory):
            self.world.add_component(ent, DropFromInventory(action.index))
            self.world.add_resource(input_action.noop)

        elif action is input_action.take_stairs:
            self.world.add_component(ent, take_stairs)
            self.world.add_resource(input_action.noop)

    def _process_basic_ai(self, ent: int) -> None:
        match = self.world.get_components(Position, Player)
        if not match:
            return
        player, (player_position, _) = match[0]
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

    def _process_confused_ai(self, ent: int, ai: ConfusedAi) -> None:
        if ai.num_turns > 0:
            random_x = randint(0, 2) - 1
            random_y = randint(0, 2) - 1

            if random_x != 0 and random_y != 0:
                self.world.add_component(
                    ent,
                    MoveOrMelee(
                        vector=Vector(random_x, random_y),
                        attack_monster=True,
                        attack_player=True,
                    ),
                )
            self.world.add_component(ent, ai.tick_down())
        else:
            self.world.add_component(ent, ai.previous_ai)
            name = self.world.component_for_entity(ent, Name)
            self.world.get_resource(Messages).append(
                f"The {name} is no longer confused!", tcod.red
            )

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

        vector = None

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x is not None and y is not None:
                vector = (Vector(x, y) - src).norm()

        if vector is None:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            vector = (dst - src).norm()

        # Delete the path to free memory
        tcod.path_delete(my_path)
        return vector
