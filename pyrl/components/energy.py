#!/usr/bin/env python

from dataclasses import dataclass


@dataclass
class Energy:
    amount: int

    def gain(self, amount: int) -> None:
        self.amount += amount

    @property
    def can_act(self) -> bool:
        return self.amount > 0

    def consume(self, amount: int) -> bool:
        if self.can_act:
            self.amount -= amount
            return True
        return False
