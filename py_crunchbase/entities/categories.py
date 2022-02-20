from .base import Entity, Collection, CardType


class Categories(Collection):

    _facet_name = 'category'
    _name = 'categories'


class CategoryCardType(CardType):
    pass


class Category(Entity):

    ENTITY_DEF_ID = 'category'
    Collection = Categories
    CardType = CategoryCardType
