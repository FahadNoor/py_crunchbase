from .base import Entity, Collection, CardType


class Investments(Collection):

    _name = 'investments'
    _facet_name = 'investment'


class InvestmentCardType(CardType):
    
    funding_round = 'funding_round'
    investor = 'investor'
    organization = 'organization'
    partner = 'partner'


class Investment(Entity):

    ENTITY_DEF_ID = 'investment'
    Collection = Investments
    CardType = InvestmentCardType
