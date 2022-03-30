from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.ownerships import Ownerships, OwnershipCards, Ownership


def test_ownerships():
    assert issubclass(Ownerships, Collection)
    assert Ownerships._name == 'ownerships'


def test_ownership_cards():
    assert issubclass(OwnershipCards, BaseCards)
    assert OwnershipCards.child_organization == 'child_organization'
    assert OwnershipCards.parent_organization == 'parent_organization'
    assert OwnershipCards.press_references == 'press_references'


def test_ownership():
    assert issubclass(Ownership, Entity)
    assert Ownership.ENTITY_DEF_ID == 'ownership'
    assert Ownership.Collection == Ownerships
    assert Ownership.Cards == OwnershipCards

