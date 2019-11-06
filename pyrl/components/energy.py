#!/usr/bin/env python

from dataclasses import dataclass, replace


class CannotActException(Exception):
    pass


@dataclass(frozen=True)
class Energy:
    amount: int

    def gain(self, amount: int) -> "Energy":
        return replace(self, amount=self.amount + amount)

    @property
    def can_act(self) -> bool:
        return self.amount > 0

    def consume(self, amount: int) -> "Energy":
        if not self.can_act:
            raise CannotActException()
        return replace(self, amount=self.amount - amount)
