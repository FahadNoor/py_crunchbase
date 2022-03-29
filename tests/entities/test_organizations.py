from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.organizations import Organizations, OrganizationCards, OrganizationFacets, Organization


def test_organizations():
    assert issubclass(Organizations, Collection)
    assert Organizations._name == 'organizations'
    assert Organizations._facet_name == 'organization'
    assert Organizations.companies == 'organization.companies'
    assert Organizations.investors == 'organization.investors'
    assert Organizations.schools == 'organization.schools'


def test_organization_cards():
    assert issubclass(OrganizationCards, BaseCards)
    assert OrganizationCards.acquiree_acquisitions == 'acquiree_acquisitions'
    assert OrganizationCards.acquirer_acquisitions == 'acquirer_acquisitions'
    assert OrganizationCards.child_organizations == 'child_organizations'
    assert OrganizationCards.child_ownerships == 'child_ownerships'
    assert OrganizationCards.event_appearances == 'event_appearances'
    assert OrganizationCards.founders == 'founders'
    assert OrganizationCards.headquarters_address == 'headquarters_address'
    assert OrganizationCards.investors == 'investors'
    assert OrganizationCards.ipos == 'ipos'
    assert OrganizationCards.jobs == 'jobs'
    assert OrganizationCards.key_employee_changes == 'key_employee_changes'
    assert OrganizationCards.layoffs == 'layoffs'
    assert OrganizationCards.parent_organization == 'parent_organization'
    assert OrganizationCards.parent_ownership == 'parent_ownership'
    assert OrganizationCards.participated_funding_rounds == 'participated_funding_rounds'
    assert OrganizationCards.participated_funds == 'participated_funds'
    assert OrganizationCards.participated_investments == 'participated_investments'
    assert OrganizationCards.press_references == 'press_references'
    assert OrganizationCards.raised_funding_rounds == 'raised_funding_rounds'
    assert OrganizationCards.raised_funds == 'raised_funds'
    assert OrganizationCards.raised_investments == 'raised_investments'


def test_organization_facets():
    assert OrganizationFacets.company == 'company'
    assert OrganizationFacets.investor == 'investor'
    assert OrganizationFacets.school == 'school'


def test_organization():
    assert issubclass(Organization, Entity)
    assert Organization.ENTITY_DEF_ID == 'organization'
    assert Organization.Collection == Organizations
    assert Organization.Cards == OrganizationCards
    assert Organization.Facets == OrganizationFacets
