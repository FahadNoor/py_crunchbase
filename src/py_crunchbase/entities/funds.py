from .base import Entity, Collection, BaseCards


class Funds(Collection):

    _name = 'funds'


class FundCards(BaseCards):
    
    investors = 'investors'
    owner = 'owner'
    press_references = 'press_references'


class Fund(Entity):

    ENTITY_DEF_ID = 'fund'
    Collection = Funds
    Cards = FundCards
