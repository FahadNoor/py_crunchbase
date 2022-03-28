from py_crunchbase.decorators import override_entity
from py_crunchbase.entities import Collection, BaseCards, Entities, Cards, Collections
from py_crunchbase.entities.organizations import Organization


def test_override_entity():
    # override Entities.Organization with SampleEntity

    class SampleCollection(Collection):
        _name = 'samples'

    class SampleCards(BaseCards):
        a_field = 'a_field'

    @override_entity(Entities.Organization)
    class SampleEntity(Entities.Organization):
        ENTITY_DEF_ID = 'sample'
        Collection = SampleCollection
        Cards = SampleCards

    assert Entities.Organization is SampleEntity
    assert Cards.Organization is SampleCards
    assert Collections.Organizations is SampleCollection
    assert Entities.entity_cls_by_id('sample') is SampleEntity

    # revert changes
    proxy = vars(Entities)['Organization']
    proxy.entity_cls = Organization
    setattr(Cards, 'Organization', Organization.Cards)
    setattr(Collections, 'Organizations', Organization.Collection)
    Entities.ENTITY_ID_CLASS_MAP = None

    assert Entities.Organization is Organization
    assert Cards.Organization is Organization.Cards
    assert Collections.Organizations is Organization.Collection
    assert Entities.entity_cls_by_id(Organization.ENTITY_DEF_ID) is Organization
