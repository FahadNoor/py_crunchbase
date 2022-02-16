from .base import Entity, Collection, Cards


class Categories(Collection):

    _facet_name = 'category'
    _name = 'categories'


class CategoryCards(Cards):
    pass


class Category(Entity):

    ENTITY_DEF_ID = 'category'
    Collection = Categories
    Cards = CategoryCards
