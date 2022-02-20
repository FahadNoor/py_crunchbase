from .base import Entity, Collection, CardType


class Events(Collection):

    _name = 'events'
    _facet_name = 'event'


class EventCardType(CardType):

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
    CardType = EventCardType
