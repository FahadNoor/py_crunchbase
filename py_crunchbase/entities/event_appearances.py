from .base import Entity, Collection, Cards


class EventAppearances(Collection):

    _name = 'event_appearances'
    _facet_name = 'event_appearance'


class EventAppearanceCards(Cards):

    event = 'event'
    participant = 'participant'


class EventAppearance(Entity):

    ENTITY_DEF_ID = 'event_appearance'
    Collection = EventAppearances
    Cards = EventAppearanceCards
