#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto


class Slot(Enum):
    MAIN_HAND = auto()
    OFF_HAND = auto()

    @property
    def name(self) -> str:
        if self is Slot.MAIN_HAND:
            return "main hand"
        if self is Slot.OFF_HAND:
            return "off hand"
        raise NotImplementedError


@dataclass
class Equippable:
    slot: Slot
    power_bonus: int = 0
    defense_bonus: int = 0
