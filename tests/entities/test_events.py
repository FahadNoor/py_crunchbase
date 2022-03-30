from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.events import Events, EventCards, Event


def test_events():
    assert issubclass(Events, Collection)
    assert Events._name == 'events'


def test_event_cards():
    assert issubclass(EventCards, BaseCards)
    assert EventCards.address == 'address'
    assert EventCards.appearances == 'appearances'
    assert EventCards.contestants == 'contestants'
    assert EventCards.exhibitors == 'exhibitors'
    assert EventCards.organizers == 'organizers'
    assert EventCards.press_references == 'press_references'
    assert EventCards.speakers == 'speakers'
    assert EventCards.sponsors == 'sponsors'


def test_event():
    assert issubclass(Event, Entity)
    assert Event.ENTITY_DEF_ID == 'event'
    assert Event.Collection is Events
    assert Event.Cards is EventCards
