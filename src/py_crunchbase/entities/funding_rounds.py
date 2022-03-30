from .base import Entity, Collection, BaseCards


class FundingRounds(Collection):

    _name = 'funding_rounds'


class FundingRoundCards(BaseCards):
    
    investments = 'investments'
    investors = 'investors'
    lead_investors = 'lead_investors'
    organization = 'organization'
    partners = 'partners'
    press_references = 'press_references'


class FundingRound(Entity):

    ENTITY_DEF_ID = 'funding_round'
    Collection = FundingRounds
    Cards = FundingRoundCards
