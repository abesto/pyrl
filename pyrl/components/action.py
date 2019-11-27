#!/usr/bin/env python

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Optional, Type

from ..vector import Vector


class Action(ABC):
    component_type: ClassVar[Type["Action"]]
    energy_cost: int


Action.component_type = Action


@dataclass(frozen=True)
class SimpleAction(Action):
    name: str
    energy_cost: int


@dataclass(frozen=True)
class Skip(Action):
    ticks: int

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:  # type: ignore
        return self.ticks


@dataclass(frozen=True)
class MoveOrMelee(Action):
    vector: Vector
    attack_player: bool
    attack_monster: bool

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:
        return int(self.vector.length)


@dataclass(frozen=True)
class UseFromInventory(Action):
    index: int
    target: Optional[Vector] = None

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:
        return 1


@dataclass(frozen=True)
class DropFromInventory(Action):
    index: int

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:
        return 1


ponder = SimpleAction("ponder", 1)
pickup = SimpleAction("pickup", 1)
skip_one = Skip(1)
