#!/usr/bin/env python3

from dataclasses import dataclass, replace

from pyrl.vector import Vector


@dataclass(frozen=True)
class Targeting:
    for_inventory_index: int
    radius: int
    current_target: Vector

    def with_current_target(self, new_target: Vector) -> "Targeting":
        if new_target != self.current_target:
            return replace(self, current_target=new_target)
        return self
