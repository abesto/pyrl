#!/usr/bin/env python3

import math
from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    unit: ClassVar[Dict[str, "Vector"]]

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    @property
    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self) -> "Vector":
        length = self.length
        if length == 0:
            return Vector(0, 0)

        nx = int(round(self.x / length))
        ny = int(round(self.y / length))
        return Vector(nx, ny)


Vector.unit = {
    "n": Vector(0, -1),
    "ne": Vector(1, -1),
    "e": Vector(1, 0),
    "se": Vector(1, 1),
    "s": Vector(0, 1),
    "sw": Vector(-1, 1),
    "w": Vector(-1, 0),
    "nw": Vector(-1, -1),
}
