#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import List

import tcod.color

from pyrl.saveload import persist_resource


@dataclass(frozen=True)
class Message:
    message: str
    color: tcod.color.Color


@dataclass
@persist_resource
class Messages:
    limit: int
    messages: List[Message] = field(default_factory=list)

    def append(self, msg: str, color: tcod.color.Color = tcod.white) -> None:
        self.messages.append(Message(msg, color))
        self.messages = self.messages[-self.limit :]

    def clear(self) -> None:
        self.messages.clear()
