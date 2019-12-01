#!/usr/bin/env python3
from dataclasses import dataclass
from random import randint
from typing import Dict, Generic, List, Tuple, TypeVar

T = TypeVar("T")


@dataclass
class SpawnRule:
    min_depth: int
    weight: int


class SpawnRow:
    def __init__(self, weight: int = 0, min_depth: int = 0):
        self.rules: List[SpawnRule] = []
        if weight != 0:
            self(weight, min_depth)
        self._dirty: bool = False

    def __call__(self, weight: int, min_depth: int = 0) -> "SpawnRow":
        self.rules.append(SpawnRule(min_depth, weight))
        self._dirty = True
        return self

    def weight(self, depth: int) -> int:
        if self._dirty:
            self.rules.sort(key=lambda r: r.min_depth, reverse=True)
        for rule in self.rules:
            if depth >= rule.min_depth:
                return rule.weight

        return 0


class SpawnTable(Generic[T]):
    def __init__(self):
        self.rules: Dict[T, SpawnRow] = {}

    def add(self, item: T) -> SpawnRow:
        row = SpawnRow()
        self.rules[item] = row
        return row

    def spawn(self, depth: int) -> T:
        choice_dict = {item: rule.weight(depth) for item, rule in self.rules.items()}
        choices = list(choice_dict.keys())
        chances = list(choice_dict.values())

        random_chance = randint(1, sum(chances))

        running_sum = 0
        for choice, w in enumerate(chances):
            running_sum += w

            if random_chance <= running_sum:
                return choices[choice]

        raise RuntimeError("We should uhhh... never reach this point in the code?")
