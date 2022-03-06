from .base import Entity, Collection, BaseCards


class Investments(Collection):

    _name = 'investments'


class InvestmentCards(BaseCards):
    
    funding_round = 'funding_round'
    investor = 'investor'
    organization = 'organization'
    partner = 'partner'


class Investment(Entity):

    ENTITY_DEF_ID = 'investment'
    Collection = Investments
    Cards = InvestmentCards
