from .base import Entity, Collection, BaseCards


class PressReferences(Collection):

    _name = 'press_references'


class PressReferenceCards(BaseCards):
    pass


class PressReference(Entity):

    ENTITY_DEF_ID = 'press_reference'
    Collection = PressReferences
    Cards = PressReferenceCards
