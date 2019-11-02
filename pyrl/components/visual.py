#!/usr/bin/env python

from dataclasses import dataclass

from tcod.color import Color


@dataclass
class Visual:
    char: str
    color: Color

    def __post_init__(self):
        self.char = self.char[0]
