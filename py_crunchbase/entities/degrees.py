from .base import Entity, Collection, CardType


class Degrees(Collection):

    _name = 'degrees'
    _facet_name = 'degree'


class DegreeCardType(CardType):
    
    organization = 'organization'
    person = 'person'


class Degree(Entity):

    ENTITY_DEF_ID = 'degree'
    Collection = Degrees
    CardType = DegreeCardType
