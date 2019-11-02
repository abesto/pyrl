#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Type


class Kind(Enum):
    Player = auto()
    Basic = auto()
    Confused = auto()


@dataclass
class Ai:
    component_type: ClassVar[Type["Ai"]]
    kind: Kind


Ai.component_type = Ai


@dataclass
class ConfusedAi(Ai):
    previoius_ai: Ai
    num_turns: int


basic = Ai(Kind.Basic)
player = Ai(Kind.Player)
