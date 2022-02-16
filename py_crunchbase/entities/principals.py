from .base import Entity, Collection


class Principals(Collection):

    _name = 'principals'
    _facet_name = 'principal'

    company = 'company'
    investor = 'investor'
    school = 'school'


class Principal(Entity):

    ENTITY_DEF_ID = 'principal'
    Collection = Principals
