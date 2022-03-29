from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.people import People, PersonCards, PersonFacets, Person


def test_people():
    assert issubclass(People, Collection)
    assert People._name == 'people'
    assert People._facet_name == 'person'
    assert People.investors == 'person.investors'


def test_person_cards():
    assert issubclass(PersonCards, BaseCards)
    assert PersonCards.degrees == 'degrees'
    assert PersonCards.event_appearances == 'event_appearances'
    assert PersonCards.founded_organizations == 'founded_organizations'
    assert PersonCards.jobs == 'jobs'
    assert PersonCards.participated_funding_rounds == 'participated_funding_rounds'
    assert PersonCards.participated_funds == 'participated_funds'
    assert PersonCards.participated_investments == 'participated_investments'
    assert PersonCards.partner_funding_rounds == 'partner_funding_rounds'
    assert PersonCards.partner_investments == 'partner_investments'
    assert PersonCards.press_references == 'press_references'
    assert PersonCards.primary_job == 'primary_job'
    assert PersonCards.primary_organization == 'primary_organization'


def test_person_facets():
    assert PersonFacets.investor == 'investor'


def test_person():
    assert issubclass(Person, Entity)
    assert Person.ENTITY_DEF_ID == 'person'
    assert Person.Collection == People
    assert Person.Cards == PersonCards
    assert Person.Facets == PersonFacets
