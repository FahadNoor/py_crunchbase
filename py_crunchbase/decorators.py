from py_crunchbase.entities import Entity, Entities, Cards, Collections


def override_entity(entity_cls):
    """
    This can be used to override any Entity class

    @override_entity(Entities.Organization):
    class CustomOrganization(Entities.Organization):
        pass

    now Entities.Organization will return CustomOrganization
    """

    def wrapper(new_entity_cls):
        if not issubclass(new_entity_cls, Entity):
            raise ValueError(f'{new_entity_cls.__name__} should be a subclass of Entity')

        attr_name = entity_cls.__name__
        proxy = vars(Entities)[attr_name]
        proxy.entity_cls = new_entity_cls
        if getattr(Cards, attr_name, None) is not None:
            setattr(Cards, attr_name, new_entity_cls.CardType)
        if getattr(Collections, attr_name, None) is not None:
            setattr(Collections, attr_name, new_entity_cls.Collection)
        return new_entity_cls

    return wrapper
