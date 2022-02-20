from .base import Entity, Collection, CardType


class Funds(Collection):

    _name = 'funds'
    _facet_name = 'fund'


class FundCardType(CardType):
    
    investors = 'investors'
    owner = 'owner'
    press_references = 'press_references'


class Fund(Entity):

    ENTITY_DEF_ID = 'fund'
    Collection = Funds
    CardType = FundCardType
