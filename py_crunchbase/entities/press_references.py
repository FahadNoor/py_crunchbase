from .base import Entity, Collection, CardType


class PressReferences(Collection):

    _name = 'press_references'
    _facet_name = 'press_reference'


class PressReferenceCardType(CardType):
    pass


class PressReference(Entity):

    ENTITY_DEF_ID = 'press_reference'
    Collection = PressReferences
    CardType = PressReferenceCardType
