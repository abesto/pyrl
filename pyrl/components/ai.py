#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Type

from pyrl.saveload import persistence_tag


class Kind(Enum):
    PLAYER = auto()
    BASIC = auto()
    CONFUSED = auto()


@dataclass(frozen=True)
@persistence_tag
class Ai:
    component_type: ClassVar[Type["Ai"]]
    kind: Kind


Ai.component_type = Ai


@dataclass(frozen=True)
class ConfusedAi(Ai):
    previous_ai: Ai
    num_turns: int

    @classmethod
    def new(cls, previous_ai: Ai, num_turns: int) -> "ConfusedAi":
        return ConfusedAi(Kind.CONFUSED, previous_ai, num_turns)

    def tick_down(self) -> "ConfusedAi":
        return ConfusedAi.new(self.previous_ai, self.num_turns - 1)


basic = Ai(Kind.BASIC)
player = Ai(Kind.PLAYER)
