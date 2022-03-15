from typing import Type

from py_crunchbase.entities import Entity, Entities, Cards, Collections


def override_entity(entity_cls: Type[Entity]):
    """
    This can be used to override any Entity class

    @override_entity(Entities.Organization)
    class CustomOrganization(Entities.Organization):
        pass

    now Entities.Organization will return CustomOrganization
    """

    def wrapper(new_entity_cls: Type[Entity]):
        if not issubclass(new_entity_cls, Entity):
            raise ValueError(f'{new_entity_cls.__name__} should be a subclass of Entity')

        # update new class in Entity's Proxy class
        entities_attr_name = cards_attr_name = entity_cls.__name__
        collections_attr_name = entity_cls.Collection.__name__
        proxy = vars(Entities)[entities_attr_name]
        proxy.entity_cls = new_entity_cls

        # update in Cards
        if getattr(Cards, cards_attr_name, None) is not None:
            setattr(Cards, cards_attr_name, new_entity_cls.Cards)

        # update in Collections
        if getattr(Collections, collections_attr_name, None) is not None:
            setattr(Collections, collections_attr_name, new_entity_cls.Collection)

        # reset Entity ID to class map
        Entities.ENTITY_ID_CLASS_MAP = None
        return new_entity_cls

    return wrapper
