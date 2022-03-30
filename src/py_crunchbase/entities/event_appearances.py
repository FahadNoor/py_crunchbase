from .base import Entity, Collection, BaseCards


class EventAppearances(Collection):

    _name = 'event_appearances'


class EventAppearanceCards(BaseCards):

    event = 'event'
    participant = 'participant'


class EventAppearance(Entity):

    ENTITY_DEF_ID = 'event_appearance'
    Collection = EventAppearances
    Cards = EventAppearanceCards
