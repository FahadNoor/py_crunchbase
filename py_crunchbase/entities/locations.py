from .base import Entity, Collection, BaseCards


class Locations(Collection):

    _name = 'locations'
    _facet_name = 'location'

    cities = 'cities'
    continents = 'continents'
    countries = 'countries'
    groups = 'groups'
    regions = 'regions'


class LocationCards(BaseCards):
    pass


class LocationFacets:

    city = 'city'
    continent = 'continent'
    country = 'country'
    group = 'group'
    region = 'region'


class Location(Entity):

    ENTITY_DEF_ID = 'location'
    Collection = Locations
    Cards = LocationCards
    Facets = LocationFacets
