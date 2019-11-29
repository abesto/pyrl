#!/usr/bin/env python

from dataclasses import dataclass

from pyrl.saveload import persistence_tag


@dataclass
@persistence_tag
class Stairs:
    to_level: int
