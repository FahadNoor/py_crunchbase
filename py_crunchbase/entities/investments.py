from .base import Entity, Collection, Cards


class Investments(Collection):

    _name = 'investments'
    _facet_name = 'investment'


class InvestmentCards(Cards):
    
    funding_round = 'funding_round'
    investor = 'investor'
    organization = 'organization'
    partner = 'partner'


class Investment(Entity):

    ENTITY_DEF_ID = 'investment'
    Collection = Investments
    Cards = InvestmentCards
