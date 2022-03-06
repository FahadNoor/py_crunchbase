from .base import Entity, Collection, BaseCards


class Categories(Collection):

    _name = 'categories'


class CategoryCards(BaseCards):
    pass


class Category(Entity):

    ENTITY_DEF_ID = 'category'
    Collection = Categories
    Cards = CategoryCards
