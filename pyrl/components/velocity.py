#!/usr/bin/env python

from dataclasses import dataclass

from ..vector import Vector


@dataclass
class Velocity:
    vector: Vector
