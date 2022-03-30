from .base import Entity, Collection, BaseCards


class CategoryGroups(Collection):

    _name = 'category_groups'


class CategoryGroupCards(BaseCards):
    pass


class CategoryGroup(Entity):

    ENTITY_DEF_ID = 'category_group'
    Collection = CategoryGroups
    Cards = CategoryGroupCards
