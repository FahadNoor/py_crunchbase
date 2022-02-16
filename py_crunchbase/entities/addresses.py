from .base import Entity, Collection, Cards


class Addresses(Collection):

    _name = 'addresses'
    _facet_name = 'address'


class AddressCards(Cards):

    event = 'event'
    organization = 'organization'


class Address(Entity):

    ENTITY_DEF_ID = 'address'
    Collection = Addresses
    Cards = AddressCards
