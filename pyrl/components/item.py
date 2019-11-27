#!/usr/bin/env python

from enum import Enum, auto


class Item(Enum):
    HEALING_POTION = auto()
    LIGHTNING_SCROLL = auto()
    FIREBALL_SCROLL = auto()
    CONFUSION_SCROLL = auto()

    @property
    def needs_targeting(self) -> bool:
        return self in [Item.FIREBALL_SCROLL, Item.CONFUSION_SCROLL]

    @property
    def targeting_radius(self) -> int:
        if self is Item.FIREBALL_SCROLL:
            return 2
        if self is Item.CONFUSION_SCROLL:
            return 0
        raise NotImplementedError
