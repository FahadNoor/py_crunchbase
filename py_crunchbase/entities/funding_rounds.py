from .base import Entity, Collection, CardType


class FundingRounds(Collection):

    _name = 'funding_rounds'
    _facet_name = 'funding_round'


class FundingRoundCardType(CardType):
    
    investments = 'investments'
    investors = 'investors'
    lead_investors = 'lead_investors'
    organization = 'organization'
    partners = 'partners'
    press_references = 'press_references'


class FundingRound(Entity):

    ENTITY_DEF_ID = 'funding_round'
    Collection = FundingRounds
    CardType = FundingRoundCardType
