#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Type


class Kind(Enum):
    Player = auto()
    Basic = auto()
    Confused = auto()


@dataclass(frozen=True)
class Ai:
    component_type: ClassVar[Type["Ai"]]
    kind: Kind


Ai.component_type = Ai


@dataclass(frozen=True)
class ConfusedAi(Ai):
    previous_ai: Ai
    num_turns: int


basic = Ai(Kind.Basic)
player = Ai(Kind.Player)
