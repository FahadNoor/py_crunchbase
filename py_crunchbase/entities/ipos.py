from .base import Entity, Collection, CardType


class Ipos(Collection):

    _name = 'ipos'
    _facet_name = 'ipo'


class IpoCardType(CardType):
    
    organization = 'organization'
    press_references = 'press_references'


class Ipo(Entity):

    ENTITY_DEF_ID = 'ipo'
    Collection = Ipos
    CardType = IpoCardType
