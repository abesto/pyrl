#!/usr/bin/env python

from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class Level:
    level_up_base: int
    level_up_factor: int
    current_level: int = 1
    current_xp: int = 0

    @property
    def experience_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, gain: int) -> "Level":
        return replace(self, current_xp=self.current_xp + gain)

    def level_up(self) -> Optional["Level"]:
        if self.current_xp < self.experience_to_next_level:
            return None

        return replace(
            self,
            current_xp=self.current_xp - self.experience_to_next_level,
            current_level=self.current_level + 1,
        )
