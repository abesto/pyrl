#!/usr/bin/env python

from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

import esper  # type: ignore
import tabulate

T = TypeVar("T")


class WorldExt(esper.World):
    def __init__(self, timed=False):
        super(WorldExt, self).__init__(timed)
        self.resources: Dict = {}

    def _process(self, *args, **kwargs):
        for processor in self._processors:
            # print(type(processor))
            processor.process(*args, **kwargs)

    def add_processors(self, *processors: "Processor"):
        for processor in processors:
            self.add_processor(processor)

    def add_resource(self, resource: T) -> None:
        resource_type = getattr(resource, "resource_type", type(resource))
        self.resources[resource_type] = resource

    def get_resource(self, resource_type: Type[T]) -> T:
        return self.resources[resource_type]

    def try_resource(self, resource_type: Type[T]) -> Optional[T]:
        return self.resources.get(resource_type, None)

    def remove_resource(self, resource_type: T) -> None:
        if resource_type in self.resources:
            del self.resources[resource_type]

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

    def add_components(self, entity: int, *component_instances: Any) -> None:
        for component in component_instances:
            self.add_component(entity, component)

    def try_component(self, entity: int, component_type: T) -> Optional[T]:
        """Try to get a single component type for an Entity.

        Copy-paste from Esper, except it returns instead of yielding, because
        yielding doesn't actually make any sense here
        """
        if component_type in self._entities[entity]:
            return self._entities[entity][component_type]
        else:
            return None


class Processor(esper.Processor):
    world: WorldExt

    def process(self, *args, **kwargs):
        raise NotImplementedError


def debug_world(world: esper.World, *with_components: Type[Any]) -> None:
    data = []
    for ent, _ in world.get_components(*with_components):
        components = world.components_for_entity(ent)
        data.append(dict({"ent": ent}, **{str(type(c)): c for c in components}))
    print(tabulate.tabulate(data))
