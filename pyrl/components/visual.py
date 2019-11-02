#!/usr/bin/env python

from dataclasses import dataclass


@dataclass
class Visual:
    char: str

    def __post_init__(self):
        self.char = self.char[0]
