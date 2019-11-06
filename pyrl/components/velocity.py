#!/usr/bin/env python

from dataclasses import dataclass

from ..vector import Vector


@dataclass(frozen=True)
class Velocity:
    vector: Vector
