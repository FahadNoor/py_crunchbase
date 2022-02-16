from .base import Entity, Collection, Cards


class Locations(Collection):

    _name = 'locations'
    _facet_name = 'location'

    city = 'city'
    continent = 'continent'
    country = 'country'
    group = 'group'
    region = 'region'


class LocationCards(Cards):
    pass


class Location(Entity):

    ENTITY_DEF_ID = 'location'
    Collection = Locations
    Cards = LocationCards
