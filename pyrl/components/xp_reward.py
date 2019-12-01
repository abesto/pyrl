#!/usr/bin/env python

from dataclasses import dataclass


@dataclass(frozen=True)
class XpReward:
    amount: int
