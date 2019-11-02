#!/usr/bin/env python

from dataclasses import dataclass

from .velocity import Heading, Velocity


@dataclass
class Position:
    x: int
    y: int

    def __iadd__(self, other: Velocity) -> "Position":
        if other.heading is Heading.West:
            self.x -= other.magnitude
        if other.heading is Heading.North:
            self.y -= other.magnitude
        if other.heading is Heading.East:
            self.x += other.magnitude
        if other.heading is Heading.South:
            self.y += other.magnitude
        return self

    def __add__(self, other: Velocity) -> "Position":
        p = Position(self.x, self.y)
        p += other
        return p
