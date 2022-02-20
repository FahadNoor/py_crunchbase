from .base import Entity, Collection, CardType


class CategoryGroups(Collection):

    _name = 'category_groups'
    _facet_name = 'category_group'

    cities = 'cities'
    regions = 'regions'
    countries = 'countries'
    groups = 'groups'


class CategoryGroupCardType(CardType):
    pass


class CategoryGroup(Entity):

    ENTITY_DEF_ID = 'category_group'
    Collection = CategoryGroups
    CardType = CategoryGroupCardType
