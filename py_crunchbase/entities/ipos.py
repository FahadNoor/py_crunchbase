from .base import Entity, Collection, BaseCards


class Ipos(Collection):

    _name = 'ipos'


class IpoCards(BaseCards):
    
    organization = 'organization'
    press_references = 'press_references'


class Ipo(Entity):

    ENTITY_DEF_ID = 'ipo'
    Collection = Ipos
    Cards = IpoCards
