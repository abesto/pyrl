#!/usr/bin/env python

from dataclasses import dataclass
from typing import ClassVar, Type


@dataclass(frozen=True)
class InputAction:
    resource_type: ClassVar[Type["InputAction"]]
    name: str


InputAction.resource_type = InputAction


noop = InputAction("noop")

move_north = InputAction("move_north")
move_east = InputAction("move_east")
move_south = InputAction("move_south")
move_west = InputAction("move_west")

quit = InputAction("quit")
