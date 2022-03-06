from .base import Entity, Collection, BaseCards


class Events(Collection):

    _name = 'events'


class EventCards(BaseCards):

    address = 'address'
    appearances = 'appearances'
    contestants = 'contestants'
    exhibitors = 'exhibitors'
    organizers = 'organizers'
    press_references = 'press_references'
    speakers = 'speakers'
    sponsors = 'sponsors'


class Event(Entity):

    ENTITY_DEF_ID = 'event'
    Collection = Events
    Cards = EventCards
