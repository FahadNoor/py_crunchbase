from abc import ABC
from typing import Tuple, Type

from .base import Entity, EntityProxy, Cards


class ER(ABC):
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
