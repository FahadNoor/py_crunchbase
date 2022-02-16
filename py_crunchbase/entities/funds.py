from .base import Entity, Collection, Cards


class Funds(Collection):

    _name = 'funds'
    _facet_name = 'fund'


class FundCards(Cards):
    
    investors = 'investors'
    owner = 'owner'
    press_references = 'press_references'


class Fund(Entity):

    ENTITY_DEF_ID = 'fund'
    Collection = Funds
    Cards = FundCards
