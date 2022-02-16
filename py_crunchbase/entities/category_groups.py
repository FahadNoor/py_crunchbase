from .base import Entity, Collection, Cards


class CategoryGroups(Collection):

    _name = 'category_groups'
    _facet_name = 'category_group'

    cities = 'cities'
    regions = 'regions'
    countries = 'countries'
    groups = 'groups'


class CategoryGroupCards(Cards):
    pass


class CategoryGroup(Entity):

    ENTITY_DEF_ID = 'category_group'
    Collection = CategoryGroups
    Cards = CategoryGroupCards
