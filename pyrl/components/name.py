#!/usr/bin/env python

from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    name: str

    def __str__(self) -> str:
        return self.name
