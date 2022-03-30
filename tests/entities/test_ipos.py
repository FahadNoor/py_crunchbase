from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.ipos import Ipos, IpoCards, Ipo


def test_ipos():
    assert issubclass(Ipos, Collection)
    assert Ipos._name == 'ipos'


def test_ipo_cards():
    assert issubclass(IpoCards, BaseCards)
    assert IpoCards.organization == 'organization'
    assert IpoCards.press_references == 'press_references'


def test_ipo():
    assert issubclass(Ipo, Entity)
    assert Ipo.ENTITY_DEF_ID == 'ipo'
    assert Ipo.Collection is Ipos
    assert Ipo.Cards is IpoCards
