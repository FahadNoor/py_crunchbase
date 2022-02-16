from .base import Entity, Collection, Cards


class Degrees(Collection):

    _name = 'degrees'
    _facet_name = 'degree'


class DegreeCards(Cards):
    
    organization = 'organization'
    person = 'person'


class Degree(Entity):

    ENTITY_DEF_ID = 'degree'
    Collection = Degrees
    Cards = DegreeCards
