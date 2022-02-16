from .base import Entity, Collection, Cards


class Events(Collection):

    _name = 'events'
    _facet_name = 'event'


class EventCards(Cards):

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
