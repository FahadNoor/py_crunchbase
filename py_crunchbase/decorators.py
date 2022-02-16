from py_crunchbase.entities import Entity, ER


def override_entity(entity_cls):
    """
    This can be used to override any Entity class

    @override_entity(ER.Organization):
    class CustomOrganization(ER.Organization):
        pass

    now ER.Organization will return CustomOrganization
    """

    def wrapper(new_entity_cls):
        if not issubclass(new_entity_cls, Entity):
            raise ValueError(f'{new_entity_cls.__name__} should be a subclass of Entity')

        proxy = vars(ER)[entity_cls.__name__]
        proxy.entity_cls = new_entity_cls
        return new_entity_cls

    return wrapper
