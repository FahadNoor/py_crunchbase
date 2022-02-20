from .base import Entity, Collection, CardType


class Addresses(Collection):

    _name = 'addresses'
    _facet_name = 'address'


class AddressCardType(CardType):

    event = 'event'
    organization = 'organization'


class Address(Entity):

    ENTITY_DEF_ID = 'address'
    Collection = Addresses
    CardType = AddressCardType
