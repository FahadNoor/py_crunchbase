from .base import Entity, Collection, BaseCards


class Organizations(Collection):

    _name = 'organizations'
    _facet_name = 'organization'

    companies = 'companies'
    investors = 'investors'
    schools = 'schools'


class OrganizationCards(BaseCards):

    acquiree_acquisitions = 'acquiree_acquisitions'
    acquirer_acquisitions = 'acquirer_acquisitions'
    child_organizations = 'child_organizations'
    child_ownerships = 'child_ownerships'
    event_appearances = 'event_appearances'
    founders = 'founders'
    headquarters_address = 'headquarters_address'
    investors = 'investors'
    ipos = 'ipos'
    jobs = 'jobs'
    key_employee_changes = 'key_employee_changes'
    layoffs = 'layoffs'
    parent_organization = 'parent_organization'
    parent_ownership = 'parent_ownership'
    participated_funding_rounds = 'participated_funding_rounds'
    participated_funds = 'participated_funds'
    participated_investments = 'participated_investments'
    press_references = 'press_references'
    raised_funding_rounds = 'raised_funding_rounds'
    raised_funds = 'raised_funds'
    raised_investments = 'raised_investments'


class OrganizationFacets:

    company = 'company'
    investor = 'investor'
    school = 'school'


class Organization(Entity):

    ENTITY_DEF_ID = 'organization'
    Collection = Organizations
    Cards = OrganizationCards
    Facets = OrganizationFacets
