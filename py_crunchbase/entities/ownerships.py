from .base import Entity, Collection, CardType


class Ownerships(Collection):

    _name = 'ownerships'
    _facet_name = 'ownership'


class OwnershipCardType(CardType):

    child_organization = 'child_organization'
    parent_organization = 'parent_organization'
    press_references = 'press_references'


class Ownership(Entity):

    ENTITY_DEF_ID = 'ownership'
    Collection = Ownerships
    CardType = OwnershipCardType
