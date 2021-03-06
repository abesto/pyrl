#!/usr/bin/env python

from dataclasses import dataclass

from pyrl.saveload import persistence_tag

from ..vector import Vector
from .velocity import Velocity


@persistence_tag
@dataclass(frozen=True)
class Position:
    vector: Vector

    @property
    def x(self) -> int:
        return self.vector.x

    @property
    def y(self) -> int:
        return self.vector.y

    def __add__(self, other: Velocity) -> "Position":
        return Position(self.vector + other.vector)
