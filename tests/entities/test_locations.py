from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.locations import Locations, LocationCards, LocationFacets, Location


def test_locations():
    assert issubclass(Locations, Collection)
    assert Locations._name == 'locations'
    assert Locations._facet_name == 'location'
    assert Locations.cities == 'location.cities'
    assert Locations.continents == 'location.continents'
    assert Locations.countries == 'location.countries'
    assert Locations.groups == 'location.groups'
    assert Locations.regions == 'location.regions'


def test_location_cards():
    assert issubclass(LocationCards, BaseCards)


def test_location_facets():
    assert LocationFacets.city == 'city'
    assert LocationFacets.continent == 'continent'
    assert LocationFacets.country == 'country'
    assert LocationFacets.group == 'group'
    assert LocationFacets.region == 'region'


def test_location():
    assert issubclass(Location, Entity)
    assert Location.ENTITY_DEF_ID == 'location'
    assert Location.Collection is Locations
    assert Location.Cards is LocationCards
    assert Location.Facets is LocationFacets
