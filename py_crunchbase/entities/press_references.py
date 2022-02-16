from .base import Entity, Collection, Cards


class PressReferences(Collection):

    _name = 'press_references'
    _facet_name = 'press_reference'


class PressReferenceCards(Cards):
    pass


class PressReference(Entity):

    ENTITY_DEF_ID = 'press_reference'
    Collection = PressReferences
    Cards = PressReferenceCards
