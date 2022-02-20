from abc import ABC
from typing import Tuple, Type

from .base import Entity, CardType, Collection


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
        for entity_cls in cls.all():
            if entity_cls.ENTITY_DEF_ID == entity_def_id:
                return entity_cls

        raise ValueError(f'No entity class found against {entity_def_id}')


class Cards(ABC):

    Acquisition = Entities.Acquisition.CardType
    Address = Entities.Address.CardType
    Category = Entities.Category.CardType
    CategoryGroup = Entities.CategoryGroup.CardType
    Degree = Entities.Degree.CardType
    EventAppearance = Entities.EventAppearance.CardType
    Event = Entities.Event.CardType
    FundingRound = Entities.FundingRound.CardType
    Fund = Entities.Fund.CardType
    Investment = Entities.Investment.CardType
    Ipo = Entities.Ipo.CardType
    Job = Entities.Job.CardType
    KeyEmployeeChange = Entities.KeyEmployeeChange.CardType
    Layoff = Entities.Layoff.CardType
    Location = Entities.Location.CardType
    Organization = Entities.Organization.CardType
    Ownership = Entities.Ownership.CardType
    Person = Entities.Person.CardType
    PressReference = Entities.PressReference.CardType
    Principal = Entities.Principal.CardType


class Collections(ABC):

    Acquisition = Entities.Acquisition.Collection
    Address = Entities.Address.Collection
    Category = Entities.Category.Collection
    CategoryGroup = Entities.CategoryGroup.Collection
    Degree = Entities.Degree.Collection
    EventAppearance = Entities.EventAppearance.Collection
    Event = Entities.Event.Collection
    FundingRound = Entities.FundingRound.Collection
    Fund = Entities.Fund.Collection
    Investment = Entities.Investment.Collection
    Ipo = Entities.Ipo.Collection
    Job = Entities.Job.Collection
    KeyEmployeeChange = Entities.KeyEmployeeChange.Collection
    Layoff = Entities.Layoff.Collection
    Location = Entities.Location.Collection
    Organization = Entities.Organization.Collection
    Ownership = Entities.Ownership.Collection
    Person = Entities.Person.Collection
    PressReference = Entities.PressReference.Collection
    Principal = Entities.Principal.Collection
