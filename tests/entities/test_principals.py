from py_crunchbase.entities import Collection, Entity
from py_crunchbase.entities.principals import Principals, PrincipalFacets, Principal


def test_principals():
    assert issubclass(Principals, Collection)
    assert Principals._name == 'principals'
    assert Principals._facet_name == 'principal'
    assert Principals.companies == 'principal.companies'
    assert Principals.investors == 'principal.investors'
    assert Principals.schools == 'principal.schools'


def test_principal_facets():
    assert PrincipalFacets.company == 'company'
    assert PrincipalFacets.investor == 'investor'
    assert PrincipalFacets.school == 'school'


def test_principal():
    assert issubclass(Principal, Entity)
    assert Principal.ENTITY_DEF_ID == 'principal'
    assert Principal.Collection == Principals
    assert Principal.Facets == PrincipalFacets
