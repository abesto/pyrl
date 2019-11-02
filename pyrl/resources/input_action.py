#!/usr/bin/env python

from typing import ClassVar, Type


class InputAction:
    resource_type: ClassVar[Type["InputAction"]]


InputAction.resource_type = InputAction


noop = InputAction()

move_north = InputAction()
move_east = InputAction()
move_south = InputAction()
move_west = InputAction()

quit = InputAction()
