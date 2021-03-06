#!/usr/bin/env python

from dataclasses import dataclass

from pyrl.saveload import persistence_tag


@persistence_tag
@dataclass(frozen=True)
class Name:
    name: str

    def __str__(self) -> str:
        return self.name
