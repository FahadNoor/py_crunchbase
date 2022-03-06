from .base import Entity, Collection, BaseCards


class Ownerships(Collection):

    _name = 'ownerships'


class OwnershipCards(BaseCards):

    child_organization = 'child_organization'
    parent_organization = 'parent_organization'
    press_references = 'press_references'


class Ownership(Entity):

    ENTITY_DEF_ID = 'ownership'
    Collection = Ownerships
    Cards = OwnershipCards
