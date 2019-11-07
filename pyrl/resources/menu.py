#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class MenuType(Enum):
    INVENTORY = auto()
    DROP = auto()


@dataclass(frozen=True)
class Menu:
    menu_type: MenuType
    header: str
    options: List[str]
    width: int
