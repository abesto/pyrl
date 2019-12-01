#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Dict, Optional, Type

from ..vector import Vector


class InputAction:
    resource_type: ClassVar[Type["InputAction"]]


InputAction.resource_type = InputAction


@dataclass(frozen=True)
class SimpleInputAction(InputAction):
    name: str


noop = SimpleInputAction("noop")
new_game = SimpleInputAction("new_game")
quit_to_main_menu = SimpleInputAction("quit_to_main_menu")
load = SimpleInputAction("load")
quit = SimpleInputAction("quit")
pickup = SimpleInputAction("pickup")
take_stairs = SimpleInputAction("take_stairs")
open_inventory = SimpleInputAction("open_inventory")
open_drop_menu = SimpleInputAction("open_drop_menu")
open_character_menu = SimpleInputAction("open_character_menu")
dismiss_menu = SimpleInputAction("close_menu")
cancel_targeting = SimpleInputAction("cancel_targeting")


@dataclass(frozen=True)
class Move(InputAction):
    vector: Vector

    one: ClassVar[Dict[str, "Move"]]


Move.one = {heading: Move(vector) for heading, vector in Vector.unit.items()}


@dataclass(frozen=True)
class Inspect(InputAction):
    vector: Vector


@dataclass(frozen=True)
class MenuChoice(InputAction):
    choice: int


@dataclass(frozen=True)
class UseFromInventory(InputAction):
    index: int
    target: Optional[Vector] = None


@dataclass(frozen=True)
class DropFromInventory(InputAction):
    index: int


class LevelUpChoice(InputAction, Enum):
    HP = auto()
    STR = auto()
    DEF = auto()
