#!/usr/bin/env python

from dataclasses import dataclass, field


@dataclass
class Fighter:
    max_hp: int = field(init=False)
    hp: int
    defense: int
    power: int

    def __post_init__(self) -> None:
        self.max_hp = self.hp
