#!/usr/bin/env python3
import functools
import inspect
from abc import ABC
from typing import Generic, Iterable, Optional, Tuple, Type, TypeVar

from pyrl.components import Energy, Equipment, Fighter, Player
from pyrl.components.action import Action
from pyrl.esper_ext import Processor, WorldExt
from pyrl.resources.input_action import InputAction, noop, quit


class RunPerActor(Processor):
    _world: WorldExt

    def __init__(self, *children: Processor):
        self.children = children

    def _get_player_that_can_act(self) -> Optional[int]:
        for ent, (_, energy) in self.world.get_components(Player, Energy):
            if energy.can_act:
                return ent
        return None

    def _player_alive(self) -> bool:
        for ent, (_, fighter) in self.world.get_components(Player, Fighter):
            # print(f"player exists. alive: {fighter.alive}")
            return fighter.alive
        # print("no player")
        return False

    def _gen_next_actor(self) -> Iterable[int]:
        # First: if the player can move, then they should
        player_that_can_act = self._get_player_that_can_act()
        if player_that_can_act:
            yield player_that_can_act
        # Second: if the player can _still_ act, then we'll stop the turn right here
        if self._get_player_that_can_act() is not None:
            return
        # Then, everyone else can act
        for ent, (energy,) in self.world.get_components(Energy):
            # Except if the player was killed in the meanwhile
            if not self._player_alive():
                return
            if energy.can_act:
                yield ent

    def _run_children(self, ent: int) -> None:
        for child in self.children:
            # print(f"  {type(child)}")
            child.process(ent)

    def process(self, *args, **kwargs) -> None:
        for next_actor in self._gen_next_actor():

            # print(f"Next: {self.world.component_for_entity(next_actor, Name)}")
            if self.world.has_component(next_actor, Player):
                have_input = self.world.try_resource(InputAction) not in (noop, quit)
                have_player_action = bool(self.world.get_components(Action, Player))
                if not (have_input or have_player_action):
                    return
            self._run_children(next_actor)

    # noinspection Mypy
    @property
    def world(self) -> WorldExt:
        return self._world

    @world.setter
    def world(self, value: WorldExt) -> None:
        self._world = value
        for child in self.children:
            child.world = value


TAction = TypeVar("TAction", bound=Action)


def can_act(world: WorldExt, ent: int) -> bool:
    energy = world.component_for_entity(ent, Energy)
    return energy.can_act


def has_action(accept_action):
    def has_action_inner(world: WorldExt, ent: int) -> bool:
        action = world.try_component(ent, Action)
        if action is None:
            return False
        if inspect.isclass(accept_action):
            return isinstance(action, accept_action)
        return action == accept_action

    return has_action_inner


def is_player(world: WorldExt, ent: int) -> bool:
    try:
        world.component_for_entity(ent, Player)
    except KeyError:
        return False
    return True


def power(world: WorldExt, ent: int) -> int:
    fighter = world.component_for_entity(ent, Fighter)
    value = fighter.power
    equipment = world.try_component(ent, Equipment)
    if equipment:
        value += equipment.power_bonus(world)
    return value


def defense(world: WorldExt, ent: int) -> int:
    fighter = world.component_for_entity(ent, Fighter)
    value = fighter.defense
    equipment = world.try_component(ent, Equipment)
    if equipment:
        value += equipment.defense_bonus(world)
    return value


def guard(*conditions):
    def wrapper(fun):
        def inner(self, ent: int, *args, **kwargs):
            if all(condition(self.world, ent) for condition in conditions):
                return fun(self, ent, *args, **kwargs)

        return inner

    return wrapper


only_player = guard(is_player)
only_monster = guard(lambda *args: not is_player(*args))


def act(accept_action):
    return guard(has_action(accept_action), can_act)


class ProcessorExt(Processor, ABC):
    @property
    def player(self) -> Optional[int]:
        matches = self.world.get_component(Player)
        if not matches:
            return None
        if len(matches) > 1:
            raise Exception(
                "More than 1 entity found with Player flag component, what gives?"
            )
        return matches[0][0]


class EntityProcessor(ProcessorExt):
    def process(self, *args, **kwargs) -> None:
        return self.process_entity(int(args[0]))

    def process_entity(self, ent: int) -> None:
        raise NotImplementedError


class ActionProcessor(EntityProcessor, Generic[TAction]):
    def process_entity(self, ent: int) -> None:
        try:
            action = self.world.component_for_entity(ent, Action)
            energy = self.world.component_for_entity(ent, Energy)
        except KeyError:
            return
        return self.process_action(ent, action, energy)

    def process_action(self, ent: int, action: TAction, energy: Energy):
        raise NotImplementedError
