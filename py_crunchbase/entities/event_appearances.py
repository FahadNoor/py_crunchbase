from .base import Entity, Collection, CardType


class EventAppearances(Collection):

    _name = 'event_appearances'
    _facet_name = 'event_appearance'


class EventAppearanceCardType(CardType):

    event = 'event'
    participant = 'participant'


class EventAppearance(Entity):

    ENTITY_DEF_ID = 'event_appearance'
    Collection = EventAppearances
    CardType = EventAppearanceCardType
