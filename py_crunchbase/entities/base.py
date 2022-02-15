import copy
from abc import ABCMeta
from collections import defaultdict
from pydoc import locate
from typing import Dict

from ..utils import DataDict, comma_spr_str_to_list


class CollectionEnumMeta(ABCMeta):

    def __new__(mcs, cls_name, bases, dict_, **kwargs):
        dict_['_name'] = dict_.pop('name')
        facet_name = dict_.pop('facet_name')
        dict_.update({id_: f'{facet_name}.{id_}' for id_ in dict_.pop('facet_ids')})
        return super().__new__(mcs, cls_name, bases, dict_, **kwargs)

    def __str__(cls):
        return cls._name


class CardEnumMeta(ABCMeta):

    def __new__(mcs, cls_name, bases, dict_, **kwargs):
        card_ids = tuple(dict_.pop('card_ids'))
        dict_.update({id_: id_ for id_ in card_ids})
        dict_['_card_ids'] = card_ids
        dict_['all'] = classmethod(lambda cls: cls._card_ids)
        return super().__new__(mcs, cls_name, bases, dict_, **kwargs)


def parse_cards(cards: Dict[str, list]):
    from .registry import EntityRegistry as ER
    parsed = defaultdict(list)
    for name, values in cards.items():
        if not values:
            parsed[name] = []
            continue
        for card in values:
            identifier = card.get('identifier', {})
            entity_def_id = identifier.get('entity_def_id')
            try:
                entity_cls = ER.get_entity_by_id(entity_def_id)
                entity = entity_cls(data={'properties': card}, uuid=identifier.get('uuid'))
            except ValueError:
                entity = DataDict(card)
            parsed[name].append(entity)
    return parsed


class Entity(DataDict):
    """
    Base class to represent all entities
    """

    API_PATH = ''
    ENTITY_DEF_ID = ''
    DEFAULT_FIELDS = tuple()

    Collection = None
    Card = None

    def __init__(self, data: dict, uuid: str = None):
        self._original_entity_data = copy.copy(data)
        self.uuid = uuid or data.get('uuid')
        data = data.get('properties', data)
        self.cards = None
        super().__init__(data)

    @property
    def cb_web_url(self) -> str:
        return f'https://www.crunchbase.com/{self.ENTITY_DEF_ID}/{self.identifier.permalink}'

    @classmethod
    def create_with_cards(cls, data: dict, cards: dict = None):
        cards = cards or data.pop('cards', {})
        data = cards.pop('fields', None) or data.get('properties') or data
        uuid = data.get('identifier', {}).get('uuid')
        entity = cls(data, uuid)
        entity.cards = parse_cards(cards) if cards else None
        return entity


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
        self.collection_id = kwargs.get('collection_id')
        self.card_ids = kwargs.get('card_ids')
        self.facet_ids = kwargs.get('facet_ids')
        self.default_fields = kwargs.get('default_fields')
        self.class_path = kwargs.get('class_path')

    def get_class_attrs(self, entity_name) -> dict:
        attrs = {'API_PATH': self.api_path, 'ENTITY_DEF_ID': self.entity_def_id}
        if self.default_fields:
            attrs['DEFAULT_FIELDS'] = tuple(comma_spr_str_to_list(self.default_fields))

        facet_ids = comma_spr_str_to_list(self.facet_ids) if self.facet_ids else []
        attrs['Collection'] = CollectionEnumMeta(f'{entity_name}CollectionEnum', (), {
            'name': self.collection_id, 'facet_name': self.entity_def_id, 'facet_ids': facet_ids
        })

        if self.card_ids:
            attrs['Card'] = CardEnumMeta(
                f'{entity_name}CardEnum', (), {'card_ids': comma_spr_str_to_list(self.card_ids)}
            )
        return attrs

    def build_by_custom_cls(self):
        cls = locate(self.class_path)
        if not cls:
            raise ValueError(f'{self.class_path} is not a valid class path for {self.name}')
        if not issubclass(cls, Entity):
            raise ValueError(f'{cls.__name__} should be a subclass of {Entity.__name__}')
        for attr, value in self.get_class_attrs(cls.__name__).items():
            setattr(cls, attr, value)
        return cls

    def build(self):
        if self.class_path:
            return self.build_by_custom_cls()
        else:
            return type(self.name, (Entity,), self.get_class_attrs(self.name))
