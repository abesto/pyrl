#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto

from tcod.color import Color


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


@dataclass(frozen=True)
class Visual:
    char: str
    color: Color
    render_order: RenderOrder
