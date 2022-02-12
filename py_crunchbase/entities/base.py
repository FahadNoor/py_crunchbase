from pydoc import locate
from typing import Iterable

from ..utils import DataDict


class CollectionMeta(type):

    def __str__(cls):
        return cls._name


class Collection(metaclass=CollectionMeta):

    def __init__(self, name: str, facet_name: str, facet_ids: Iterable):
        self._name = name
        for id_ in facet_ids:
            setattr(self, id_, f'{facet_name}.{id_}')

    def __str__(self):
        return self._name


class Entity(DataDict):
    """
    Base class to represent all entities
    """

    API_PATH = ''
    ENTITY_DEF_ID = ''
    DEFAULT_FIELDS = tuple()
    FACET_IDS = tuple()

    def __init__(self, data: dict, uuid: str = None, cards: dict = None):
        self._original_entity_data = data
        self.uuid = uuid or data.get('uuid')
        cards = cards or data.get('cards')
        self.cards = DataDict(cards) if isinstance(cards, dict) else cards
        data = data.get('properties', data)
        super().__init__(data)

    @property
    def cb_web_url(self) -> str:
        return f'https://www.crunchbase.com/{self.ENTITY_DEF_ID}/{self.identifier.permalink}'

    @classmethod
    def as_collection(cls):
        return Collection(cls.API_PATH, cls.ENTITY_DEF_ID, cls.FACET_IDS)


class EntityBuilder:
    """
    This can build new or set an existing class to be used as an entity class.

    - if class_path is provided, then class from this path is loaded and return after setting default attributes
        - this class must be inherited from Entity class

    - if class_path is not provided, then a new class is returned that inherits from Entity
    """

    def __init__(self, name: str, api_path: str, entity_def_id: str, **kwargs):
        self.name = name
        self.api_path = api_path
        self.entity_def_id = entity_def_id
        self.facet_ids = kwargs.get('facet_ids')
        self.default_fields = kwargs.get('default_fields')
        self.class_path = kwargs.get('class_path')

    def get_class_attrs(self) -> dict:
        attrs = {'API_PATH': self.api_path, 'ENTITY_DEF_ID': self.entity_def_id}
        if self.facet_ids:
            attrs['FACET_IDS'] = tuple(self.facet_ids.split(','))
        if self.default_fields:
            attrs['DEFAULT_FIELDS'] = tuple(self.default_fields.split(','))
        return attrs

    def build_by_custom_cls(self):
        cls = locate(self.class_path)
        if not cls:
            raise ValueError(f'{self.class_path} is not a valid class path for {self.name}')
        if not issubclass(cls, Entity):
            raise ValueError(f'{cls.__name__} should be a subclass of {Entity.__name__}')
        for attr, value in self.get_class_attrs().items():
            setattr(cls, attr, value)
        return cls

    def build(self):
        if self.class_path:
            return self.build_by_custom_cls()
        else:
            return type(self.name, (Entity,), self.get_class_attrs())
