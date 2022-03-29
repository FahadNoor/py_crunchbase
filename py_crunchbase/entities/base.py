import copy
import os.path
from abc import ABCMeta, abstractmethod, ABC

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

        facet_name = dict_.get('_facet_name')
        if facet_name:
            for attr_name, value in dict_.items():
                if attr_name[0] != '_':
                    dict_[attr_name] = f'{facet_name}.{value}'

        return super().__new__(mcs, cls_name, bases, dict_)

    def __str__(cls):
        return cls._name


class Collection(metaclass=CollectionMeta):

    _name = ''
    _facet_name = ''

    @abstractmethod
    def __init__(self):
        pass


# Card #
class BaseCards(ABC):

    fields = 'fields'

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def all(cls):
        """returns a tuple of all card values."""
        names = (name for name in dir(cls) if not name.startswith('_') and name != 'all')
        return tuple(getattr(cls, name) for name in names)


# Entity #
class Entity(DataDict):
    """
    Base class to represent all entities
    """

    ENTITY_DEF_ID = ''
    Collection = None
    Cards = None
    Facets = None

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
