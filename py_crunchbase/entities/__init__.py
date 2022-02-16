from abc import ABCMeta
from typing import Tuple, Type

from .base import Entity, EntityProxy


class ERMeta(ABCMeta):

    def __new__(mcs, cls_name, bases, dict_):
        dict_['all'] = classmethod(
            lambda cls: tuple(getattr(cls, key) for key, value in dict_.items() if isinstance(value, EntityProxy))
        )
        return super().__new__(mcs, cls_name, bases, dict_)


class ER(metaclass=ERMeta):
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
        return tuple()
