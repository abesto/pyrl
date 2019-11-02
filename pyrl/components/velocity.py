#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto


class Heading(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


@dataclass
class Velocity:
    heading: Heading
    magnitude: int
