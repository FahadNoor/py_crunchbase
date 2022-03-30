from .base import Entity, Collection, BaseCards


class Degrees(Collection):

    _name = 'degrees'


class DegreeCards(BaseCards):
    
    organization = 'organization'
    person = 'person'


class Degree(Entity):

    ENTITY_DEF_ID = 'degree'
    Collection = Degrees
    Cards = DegreeCards
