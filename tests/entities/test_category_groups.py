from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.category_groups import CategoryGroups, CategoryGroupCards, CategoryGroup


def test_category_groups():
    assert issubclass(CategoryGroups, Collection)
    assert CategoryGroups._name == 'category_groups'


def test_category_group_cards():
    assert issubclass(CategoryGroupCards, BaseCards)


def test_category_group():
    assert issubclass(CategoryGroup, Entity)
    assert CategoryGroup.ENTITY_DEF_ID == 'category_group'
    assert CategoryGroup.Collection is CategoryGroups
    assert CategoryGroup.Cards is CategoryGroupCards
