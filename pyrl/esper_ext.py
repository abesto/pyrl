#!/usr/bin/env python

from typing import Any, Dict, Optional, Type, TypeVar

import esper  # type: ignore

T = TypeVar("T")


class WorldExt(esper.World):
    def __init__(self, timed=False):
        super(WorldExt, self).__init__(timed)
        self.resources: Dict = {}

    def add_processors(self, *processors: "Processor"):
        for idx, processor in enumerate(reversed(processors)):
            self.add_processor(processor, idx)

    def add_resource(self, resource: T) -> None:
        resource_type = getattr(resource, "resource_type", type(resource))
        self.resources[resource_type] = resource

    def get_resource(self, resource_type: Type[T]) -> T:
        return self.resources[resource_type]

    def try_resource(self, resource_type: Type[T]) -> Optional[T]:
        return self.resources.get(resource_type, None)

    def add_component(self, entity: int, component_instance: Any) -> None:
        """Add a new Component instance to an Entity.

        Copy-paste from Esper, but supports overriding the component type.

        :param entity: The Entity to associate the Component with.
        :param component_instance: A Component instance.
        """
        component_type = getattr(
            component_instance, "component_type", type(component_instance)
        )

        if component_type not in self._components:
            self._components[component_type] = set()

        self._components[component_type].add(entity)

        if entity not in self._entities:
            self._entities[entity] = {}

        self._entities[entity][component_type] = component_instance
        self.clear_cache()


class Processor(esper.Processor):
    world: WorldExt

    def process(self, *args, **kwargs):
        raise NotImplementedError
