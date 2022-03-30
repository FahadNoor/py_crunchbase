from .base import Entity, Collection, BaseCards


class People(Collection):

    _name = 'people'
    _facet_name = 'person'

    investors = 'investors'


class PersonCards(BaseCards):

    degrees = 'degrees'
    event_appearances = 'event_appearances'
    founded_organizations = 'founded_organizations'
    jobs = 'jobs'
    participated_funding_rounds = 'participated_funding_rounds'
    participated_funds = 'participated_funds'
    participated_investments = 'participated_investments'
    partner_funding_rounds = 'partner_funding_rounds'
    partner_investments = 'partner_investments'
    press_references = 'press_references'
    primary_job = 'primary_job'
    primary_organization = 'primary_organization'


class PersonFacets:

    investor = 'investor'


class Person(Entity):

    ENTITY_DEF_ID = 'person'
    Collection = People
    Cards = PersonCards
    Facets = PersonFacets
