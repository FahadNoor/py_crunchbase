from typing import Type

from .base import Resource


def create_resource(name: str, api_path: str, entity_def_id: str):
    return type(name, (Resource,), {'API_PATH': api_path, 'ENTITY_DEF_ID': entity_def_id})


class ResourceRegistryMeta(type):

    def __new__(mcs, cls_name, bases, dict_):
        dict_['_NAME_MAP'] = {
            res_name: create_resource(res_name, api_path, entity_def_id)
            for res_name, (api_path, entity_def_id) in dict_['_NAME_MAP'].items()
        }
        dict_['_ENTITY_ID_MAP'] = {resource.ENTITY_DEF_ID: resource for resource in dict_['_NAME_MAP'].values()}
        return type.__new__(mcs, cls_name, bases, dict_)

    def __getattr__(cls, name):
        try:
            return cls.get_resource_by_name(name)
        except ValueError:
            raise AttributeError


class ResourceRegistry(metaclass=ResourceRegistryMeta):
    """
    ResourceRegistry contains information about all CB resource classes
        ResourceRegistry.Organization will return class that represents Organization
        ResourceRegistry.Person returns a Person class

    _NAME_MAP: holds a map between resource names and respective classes
        _NAME_MAP = {
            'Organization': Organization,
            'Person': Person,
        }

    _ENTITY_ID_MAP: holds a map between resources entity ids and respective classes
        _ENTITY_ID_MAP = {
            'organization': Organization,
            'person': Person,
        }
    """

    _NAME_MAP = {
        # Resource Name: (api_path, entity_def_id)

        'Organization': ('organizations', 'organization'),
        'Person': ('people', 'person'),
        'FundingRound': ('funding_rounds', 'funding_round'),
        'Acquisition': ('acquisitions', 'acquisition'),
        'Investment': ('investments', 'investment'),
        'Event': ('events', 'event'),
        'PressReference': ('press_references', 'press_reference'),
        'Fund': ('funds', 'fund'),
        'EventAppearance': ('event_appearances', 'event_appearance'),
        'Ipo': ('ipos', 'ipo'),
        'Ownership': ('ownerships', 'ownership'),
        'Category': ('categories', 'category'),
        'CategoryGroup': ('category_groups', 'category_group'),
        'Location': ('locations', 'location'),
        'Job': ('jobs', 'job'),
        'KeyEmployeeChange': ('key_employee_changes', 'key_employee_change'),
        'Layoff': ('layoffs', 'layoff'),
        'Address': ('addresses', 'address'),
        'Degree': ('degrees', 'degree'),
        'Principal': ('principals', 'principal'),
    }

    _ENTITY_ID_MAP = {}

    @classmethod
    def get_resource_by_name(cls, name: str) -> Type[Resource]:
        """
        returns resource class by its name
        """
        resource = cls._NAME_MAP.get(name)
        if resource is None:
            raise ValueError(f"Resource {name} doesn't exist.")
        return resource

    @classmethod
    def get_resource_by_id(cls, entity_def_id: str) -> Type[Resource]:
        """
        returns resource class by its entity_def_id
        """
        resource = cls._ENTITY_ID_MAP.get(entity_def_id)
        if resource is None:
            raise ValueError(f"Resource with ID {entity_def_id} doesn't exist.")
        return resource

    @classmethod
    def add_resource(cls, resource_cls: Type[Resource], name: str = None):
        name = name or resource_cls.__name__
        if not issubclass(resource_cls, Resource):
            raise ValueError(f'{resource_cls.__name__} should be a child class of {Resource.__name__}')
        cls._NAME_MAP[name] = resource_cls
        cls._ENTITY_ID_MAP[resource_cls.ENTITY_DEF_ID] = resource_cls
