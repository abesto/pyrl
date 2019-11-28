#!/usr/bin/env python

from dataclasses import dataclass, field, replace
from typing import Dict, List

from pyrl.saveload import PostprocessedComponent


class InventoryFullException(Exception):
    pass


@dataclass(frozen=True)
class Inventory(PostprocessedComponent):
    capacity: int
    items: List[int] = field(default_factory=list)

    def add(self, item: int) -> "Inventory":
        if len(self.items) + 1 > self.capacity:
            raise InventoryFullException()
        return replace(self, items=self.items + [item])

    def remove_item_at(self, index: int) -> "Inventory":
        return replace(self, items=self.items[:index] + self.items[index + 1 :])

    def postprocess(self, entity_map: Dict[int, int]) -> "Inventory":
        return replace(self, items=[entity_map[entity] for entity in self.items])
