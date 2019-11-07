#!/usr/bin/env python

from dataclasses import dataclass, field
from typing import ClassVar, Dict, Type

from ..vector import Vector


class InputAction:
    resource_type: ClassVar[Type["InputAction"]]


InputAction.resource_type = InputAction


@dataclass
class SimpleInputAction(InputAction):
    name: str


noop = SimpleInputAction("noop")
quit = SimpleInputAction("quit")


@dataclass(frozen=True)
class Move(InputAction):
    vector: Vector

    one: ClassVar[Dict[str, "Move"]]


Move.one = {heading: Move(vector) for heading, vector in Vector.unit.items()}


@dataclass(frozen=True)
class Inspect(InputAction):
    vector: Vector
