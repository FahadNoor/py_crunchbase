from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.event_appearances import EventAppearances, EventAppearanceCards, EventAppearance


def test_event_appearances():
    assert issubclass(EventAppearances, Collection)
    assert EventAppearances._name == 'event_appearances'


def test_event_appearance_cards():
    assert issubclass(EventAppearanceCards, BaseCards)
    assert EventAppearanceCards.event == 'event'
    assert EventAppearanceCards.participant == 'participant'


def test_event_appearance():
    assert issubclass(EventAppearance, Entity)
    assert EventAppearance.ENTITY_DEF_ID == 'event_appearance'
    assert EventAppearance.Collection is EventAppearances
    assert EventAppearance.Cards is EventAppearanceCards
