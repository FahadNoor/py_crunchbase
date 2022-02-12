import configparser
from pathlib import Path
from typing import Type, Dict

from .base import Entity, EntityBuilder


def build_entities() -> Dict[str, Type[Entity]]:
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent / 'entities.ini'
    config.read(config_path)
    return {
        entity_name: EntityBuilder(entity_name, **config[entity_name]).build()
        for entity_name in config.sections()
    }


class EntityRegistryMeta(type):

    def __new__(mcs, cls_name, bases, dict_):
        entities = build_entities()
        dict_.update(entities)
        dict_['ID_ENTITY_MAP'] = {entity.ENTITY_DEF_ID: entity for entity in entities.values()}
        return type.__new__(mcs, cls_name, bases, dict_)


class EntityRegistry(metaclass=EntityRegistryMeta):
    """
    EntityRegistry contains information about all CB entities classes
        EntityRegistry.Organization will return class that represents Organization
        EntityRegistry.Person returns a Person class

    ID_ENTITY_MAP: holds a map between entities entity ids and respective classes
        ID_ENTITY_MAP = {
            'organization': Organization,
            'person': Person,
        }
    """

    ID_ENTITY_MAP = {}

    @classmethod
    def get_entity_by_id(cls, entity_def_id: str) -> Type[Entity]:
        """
        returns resource class by its entity_def_id
        """
        resource = cls.ID_ENTITY_MAP.get(entity_def_id)
        if resource is None:
            raise ValueError(f"Entity with ID {entity_def_id} doesn't exist.")
        return resource

    @classmethod
    def all(cls):
        return cls.ID_ENTITY_MAP.values()
