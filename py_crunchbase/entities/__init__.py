from abc import ABC, abstractmethod
from typing import Tuple, Type, Union

from .base import Entity, BaseCards, Collection
from ..utils import DataDict


class EntityProxy:

    def __init__(self, entity_cls: Type[Entity]):
        self.entity_cls = entity_cls

    def __get__(self, instance, owner) -> Type[Entity]:
        return self.entity_cls


class Entities(ABC):
    """
    This class should be used to access any or all Entity classes

    EntityProxy and override_entity decorator work together to provide the ability to extend Entity classes.
    """
    from .acquisitions import Acquisition
    from .addresses import Address
    from .categories import Category
    from .category_groups import CategoryGroup
    from .degrees import Degree
    from .event_appearances import EventAppearance
    from .events import Event
    from .funding_rounds import FundingRound
    from .funds import Fund
    from .investments import Investment
    from .ipos import Ipo
    from .jobs import Job
    from .key_employee_changes import KeyEmployeeChange
    from .layoffs import Layoff
    from .locations import Location
    from .organizations import Organization
    from .ownerships import Ownership
    from .people import Person
    from .press_references import PressReference
    from .principals import Principal

    @abstractmethod
    def __init__(self):
        pass
    
    ENTITY_ID_CLASS_MAP = None

    Acquisition = EntityProxy(Acquisition)
    Address = EntityProxy(Address)
    Category = EntityProxy(Category)
    CategoryGroup = EntityProxy(CategoryGroup)
    Degree = EntityProxy(Degree)
    EventAppearance = EntityProxy(EventAppearance)
    Event = EntityProxy(Event)
    FundingRound = EntityProxy(FundingRound)
    Fund = EntityProxy(Fund)
    Investment = EntityProxy(Investment)
    Ipo = EntityProxy(Ipo)
    Job = EntityProxy(Job)
    KeyEmployeeChange = EntityProxy(KeyEmployeeChange)
    Layoff = EntityProxy(Layoff)
    Location = EntityProxy(Location)
    Organization = EntityProxy(Organization)
    Ownership = EntityProxy(Ownership)
    Person = EntityProxy(Person)
    PressReference = EntityProxy(PressReference)
    Principal = EntityProxy(Principal)

    @classmethod
    def all(cls) -> Tuple[Type[Entity]]:
        # noinspection PyTypeChecker
        return tuple(getattr(cls, key) for key, value in cls.__dict__.items() if isinstance(value, EntityProxy))

    @classmethod
    def entity_cls_by_id(cls, entity_def_id: str) -> Type[Entity]:
        if cls.ENTITY_ID_CLASS_MAP is None:
            cls.ENTITY_ID_CLASS_MAP = {
                entity_cls.ENTITY_DEF_ID: entity_cls
                for entity_cls in cls.all()
            }
        
        entity_cls = cls.ENTITY_ID_CLASS_MAP.get(entity_def_id)
        if entity_cls is None:
            raise ValueError(f'No entity class found against {entity_def_id}')
        return entity_cls

    @classmethod
    def dict_to_entity(cls, data: dict) -> Union[Entity, DataDict]:
        entity_def_id = data.get('identifier', {}).get('entity_def_id')
        try:
            return cls.entity_cls_by_id(entity_def_id)(data)
        except ValueError:
            return DataDict(data)


class Cards(ABC):

    Acquisition = Entities.Acquisition.Cards
    Address = Entities.Address.Cards
    Category = Entities.Category.Cards
    CategoryGroup = Entities.CategoryGroup.Cards
    Degree = Entities.Degree.Cards
    EventAppearance = Entities.EventAppearance.Cards
    Event = Entities.Event.Cards
    FundingRound = Entities.FundingRound.Cards
    Fund = Entities.Fund.Cards
    Investment = Entities.Investment.Cards
    Ipo = Entities.Ipo.Cards
    Job = Entities.Job.Cards
    KeyEmployeeChange = Entities.KeyEmployeeChange.Cards
    Layoff = Entities.Layoff.Cards
    Location = Entities.Location.Cards
    Organization = Entities.Organization.Cards
    Ownership = Entities.Ownership.Cards
    Person = Entities.Person.Cards
    PressReference = Entities.PressReference.Cards
    Principal = Entities.Principal.Cards


class Collections(ABC):

    Acquisitions = Entities.Acquisition.Collection
    Addresses = Entities.Address.Collection
    Categories = Entities.Category.Collection
    CategoryGroups = Entities.CategoryGroup.Collection
    Degrees = Entities.Degree.Collection
    EventAppearances = Entities.EventAppearance.Collection
    Events = Entities.Event.Collection
    FundingRounds = Entities.FundingRound.Collection
    Funds = Entities.Fund.Collection
    Investments = Entities.Investment.Collection
    Ipos = Entities.Ipo.Collection
    Jobs = Entities.Job.Collection
    KeyEmployeeChanges = Entities.KeyEmployeeChange.Collection
    Layoffs = Entities.Layoff.Collection
    Locations = Entities.Location.Collection
    Organizations = Entities.Organization.Collection
    Ownerships = Entities.Ownership.Collection
    People = Entities.Person.Collection
    PressReferences = Entities.PressReference.Collection
    Principals = Entities.Principal.Collection
