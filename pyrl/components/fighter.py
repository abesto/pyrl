#!/usr/bin/env python

from dataclasses import dataclass, field, replace
from typing import Optional


@dataclass(frozen=True)
class Fighter:
    max_hp: int
    hp: int
    defense: int
    power: int

    @classmethod
    def new(
        cls, hp: int, defense: int, power: int, max_hp: Optional[int] = None
    ) -> "Fighter":
        return Fighter(max_hp or hp, hp, defense, power)

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int) -> "Fighter":
        return replace(self, hp=min(self.max_hp, self.hp + amount))

    def take_damage(self, amount: int) -> "Fighter":
        return replace(self, hp=max(0, self.hp - amount))
