from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.press_references import PressReferences, PressReferenceCards, PressReference


def test_press_references():
    assert issubclass(PressReferences, Collection)
    assert PressReferences._name == 'press_references'


def test_press_reference_cards():
    assert issubclass(PressReferenceCards, BaseCards)


def test_press_reference():
    assert issubclass(PressReference, Entity)
    assert PressReference.ENTITY_DEF_ID == 'press_reference'
    assert PressReference.Collection == PressReferences
    assert PressReference.Cards == PressReferenceCards
