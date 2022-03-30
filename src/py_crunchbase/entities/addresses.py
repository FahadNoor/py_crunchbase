from .base import Entity, Collection, BaseCards


class Addresses(Collection):

    _name = 'addresses'


class AddressCards(BaseCards):

    event = 'event'
    organization = 'organization'


class Address(Entity):

    ENTITY_DEF_ID = 'address'
    Collection = Addresses
    Cards = AddressCards
