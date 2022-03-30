from .base import Entity, Collection


class Layoffs(Collection):

    _name = 'layoffs'


class Layoff(Entity):

    ENTITY_DEF_ID = 'layoff'
    Collection = Layoffs
