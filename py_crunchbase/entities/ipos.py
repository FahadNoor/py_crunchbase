from .base import Entity, Collection, Cards


class Ipos(Collection):

    _name = 'ipos'
    _facet_name = 'ipo'


class IpoCards(Cards):
    
    organization = 'organization'
    press_references = 'press_references'


class Ipo(Entity):

    ENTITY_DEF_ID = 'ipo'
    Collection = Ipos
    Cards = IpoCards
