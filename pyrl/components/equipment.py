#!/usr/bin/env python
from dataclasses import dataclass
from typing import Mapping, Optional

from pyrl.components.equippable import Equippable, Slot
from pyrl.esper_ext import WorldExt


@dataclass
class Equipment:
    # The mapping direction is counter-intuitive, but it turns out we don't ever use the other direction
    # (currently at least)
    _items: Mapping[int, Slot]

    def _equippable(self, world: WorldExt, ent: int) -> Equippable:
        return world.component_for_entity(ent, Equippable)

    def _bonus(self, world: WorldExt, field: str) -> int:
        value = 0
        for item in self._items.keys():
            try:
                equippable = self._equippable(world, item)
            except KeyError:
                pass
            else:
                value += getattr(equippable, field)
        return value

    def power_bonus(self, world: WorldExt) -> int:
        return self._bonus(world, "power_bonus")

    def defense_bonus(self, world: WorldExt) -> int:
        return self._bonus(world, "defense_bonus")

    def toggle_equip(self, world: WorldExt, ent: int) -> "Equipment":
        if self.is_equipped(ent):
            return self.unequip(ent)
        else:
            return self.equip(world, ent)

    def unequip(self, ent: int) -> "Equipment":
        return Equipment(
            {item: slot for item, slot in self._items.items() if item != ent}
        )

    def equip(self, world: WorldExt, ent: int) -> "Equipment":
        equippable = self._equippable(world, ent)
        return Equipment(dict(list(self._items.items()) + [(ent, equippable.slot)]))

    def is_equipped(self, ent: int) -> bool:
        return ent in self._items

    def equipped_to(self, ent: int) -> Optional[Slot]:
        if not self.is_equipped(ent):
            return None
        return self._items.get(ent, None)
