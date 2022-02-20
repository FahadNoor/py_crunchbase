import copy
import os.path
from abc import ABCMeta

from ..constants import CB_WEBSITE_URL
from ..utils import DataDict


# Collection #
class CollectionMeta(ABCMeta):
    """
    - appends Collection._facet_name at the start of all facet values
        if _facet_name is organization then companies will become organization.companies
    - overrides __str__ for collection so that str(Collection) returns cls._name
    """

    def __new__(mcs, cls_name, bases, dict_):

        facet_name = dict_['_facet_name']
        for attr_name, value in dict_.items():
            if attr_name[0] != '_':
                dict_[attr_name] = f'{facet_name}.{value}'

        return super().__new__(mcs, cls_name, bases, dict_)

    def __str__(cls):
        return cls._name


class Collection(metaclass=CollectionMeta):

    _name = ''
    _facet_name = ''


# Card #
class CardTypeMeta(ABCMeta):

    def __new__(mcs, cls_name, bases, dict_):
        dict_.pop('all', None)
        all_values = tuple(value for key, value in dict_.items() if not key.startswith('__'))
        dict_['all'] = classmethod(lambda cls: all_values)
        return super().__new__(mcs, cls_name, bases, dict_)


class CardType(metaclass=CardTypeMeta):

    fields = 'fields'

    @classmethod
    def all(cls):
        """returns a tuple of all card values. It will be updated in metaclass"""
        return tuple()


# Entity #
class Entity(DataDict):
    """
    Base class to represent all entities
    """

    ENTITY_DEF_ID = ''
    Collection = None
    CardType = None

    # same fields are being used/fetched in multiple use cases, they can be defined here in order to reuse them
    # in the APIs
    DEFAULT_FIELDS = tuple()

    def __init__(self, data: dict):
        self._original_entity_data = copy.copy(data)
        self.cards = None
        super().__init__(data)

    @property
    def uuid(self) -> str:
        return self.identifier.uuid or ''

    @property
    def permalink(self) -> str:
        return self.identifier.permalink or ''

    @property
    def entity_def_id(self) -> str:
        return self.ENTITY_DEF_ID or self.identifier.entity_def_id or ''

    @property
    def web_url(self) -> str:
        return os.path.join(CB_WEBSITE_URL, self.entity_def_id, self.permalink)

    @classmethod
    def api_path(cls) -> str:
        return str(cls.Collection)
