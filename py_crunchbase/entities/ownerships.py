from .base import Entity, Collection, Cards


class Ownerships(Collection):

    _name = 'ownerships'
    _facet_name = 'ownership'


class OwnershipCards(Cards):

    child_organization = 'child_organization'
    parent_organization = 'parent_organization'
    press_references = 'press_references'


class Ownership(Entity):

    ENTITY_DEF_ID = 'ownership'
    Collection = Ownerships
    Cards = OwnershipCards
