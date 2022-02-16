from .base import Entity, Collection


class Layoffs(Collection):

    _name = 'layoffs'
    _facet_name = 'layoff'


class Layoff(Entity):

    ENTITY_DEF_ID = 'layoff'
    Collection = Layoffs
