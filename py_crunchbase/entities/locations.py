from .base import Entity, Collection, CardType


class Locations(Collection):

    _name = 'locations'
    _facet_name = 'location'

    city = 'city'
    continent = 'continent'
    country = 'country'
    group = 'group'
    region = 'region'


class LocationCardType(CardType):
    pass


class Location(Entity):

    ENTITY_DEF_ID = 'location'
    Collection = Locations
    CardType = LocationCardType
