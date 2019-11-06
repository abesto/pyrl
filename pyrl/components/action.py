#!/usr/bin/env python

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Type

from ..vector import Vector


class Action(ABC):
    component_type: ClassVar[Type["Action"]]
    energy_cost: int


Action.component_type = Action


@dataclass
class SimpleAction(Action):
    name: str
    energy_cost: int


@dataclass
class Skip(Action):
    ticks: int

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:  # type: ignore
        return self.ticks


@dataclass
class MoveOrMelee(Action):
    vector: Vector
    attack_player: bool
    attack_monster: bool

    # https://github.com/python/mypy/issues/4125
    @property
    def energy_cost(self) -> int:  # type: ignore
        return int(self.vector.length)


ponder = SimpleAction("ponder", 1)
skip_one = Skip(1)
