#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum

from tcod.color import Color


class RenderOrder(Enum):
    Corpse = 1
    Item = 2
    Actor = 3


@dataclass(frozen=True)
class Visual:
    char: str
    color: Color
    render_order: RenderOrder
