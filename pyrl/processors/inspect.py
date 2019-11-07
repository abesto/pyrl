#!/usr/bin/env python

from typing import List

from pyrl.components import Name, Position
from pyrl.esper_ext import Processor
from pyrl.resources import Fov, Messages
from pyrl.resources.input_action import InputAction, Inspect, noop


class InspectProcessor(Processor):
    def process(self):
        input_action = self.world.get_resource(InputAction)
        if not isinstance(input_action, Inspect):
            return

        fov_map = self.world.get_resource(Fov).fov_map
        names: List[str] = []
        for _, (name, position) in self.world.get_components(Name, Position):
            if position.vector != input_action.vector:
                continue
            if not fov_map.fov[position.y, position.x]:
                continue
            names.append(str(name).capitalize())

        if names:
            messages = self.world.get_resource(Messages)
            messages.append(", ".join(names))

        self.world.add_resource(noop)
