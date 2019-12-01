#!/usr/bin/env python
import gzip
import pickle
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Type, TypeVar

from pyrl import config
from pyrl.esper_ext import WorldExt

resource_types: List[Type[Any]] = []
tag_component_types: List[Type[Any]] = []
postprocessed_component_types: List[Type["PostprocessedComponent"]] = []


def persist_resource(resource_type: Type[Any]):
    """
    Decorate resource classes to be persisted in save files
    """
    resource_types.append(resource_type)
    return resource_type


def persistence_tag(component_type: Type[Any]):
    """
    Decorate components that tag entities for persistence
    """
    tag_component_types.append(component_type)
    return component_type


T = TypeVar("T", bound="PostprocessedComponent")


class PostprocessedComponent:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        postprocessed_component_types.append(cls)

    @abstractmethod
    def postprocess(self: T, entity_map: Dict[int, int]) -> T:
        raise NotImplementedError


@dataclass
class Savedata:
    resources: List[Any]
    entities: Dict[int, List[Any]]


def save(world: WorldExt) -> None:
    savedata = Savedata(
        resources=[
            resource
            for resource in [
                world.try_resource(resource_type) for resource_type in resource_types
            ]
            if resource is not None
        ],
        entities={
            entity: world.components_for_entity(entity)
            for component_type in tag_component_types
            for entity, _ in world.get_component(component_type)
        },
    )
    config.SAVEFILE.parent.mkdir(exist_ok=True, parents=True)
    with gzip.open(config.SAVEFILE, "w") as f:
        pickle.dump(savedata, f)


def load(world: WorldExt) -> bool:
    # In extreme cases we might run into issues where entity IDs become extremely huge.
    # Might be good to compact entity IDs from time to time or whatever ;)
    try:
        with gzip.open(config.SAVEFILE, "r") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        return False
    else:
        for resource in data.resources:
            world.add_resource(resource)
        entity_map: Dict[int, int] = {}
        for entity, components in data.entities.items():
            entity_map[entity] = world.create_entity(*components)
        for component_type in postprocessed_component_types:
            for entity, component in world.get_component(component_type):
                world.add_component(entity, component.postprocess(entity_map))
        return True
