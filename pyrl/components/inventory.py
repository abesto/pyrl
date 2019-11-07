#!/usr/bin/env python

from dataclasses import dataclass, field, replace
from typing import List


class InventoryFullException(Exception):
    pass


@dataclass(frozen=True)
class Inventory:
    capacity: int
    items: List[int] = field(default_factory=list)

    def add(self, item: int) -> "Inventory":
        if len(self.items) + 1 > self.capacity:
            raise InventoryFullException()
        return replace(self, items=self.items + [item])

    def remove_item_at(self, index: int) -> "Inventory":
        return replace(self, items=self.items[:index] + self.items[index + 1 :])
