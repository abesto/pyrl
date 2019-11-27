#!/usr/bin/env python

from enum import Enum, auto


class Item(Enum):
    HEALING_POTION = auto()
    LIGHTNING_SCROLL = auto()
    FIREBALL_SCROLL = auto()

    @property
    def needs_targeting(self) -> bool:
        return self in [Item.FIREBALL_SCROLL]