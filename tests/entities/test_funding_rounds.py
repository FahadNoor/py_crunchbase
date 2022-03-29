from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.funding_rounds import FundingRounds, FundingRoundCards, FundingRound


def test_funding_rounds():
    assert issubclass(FundingRounds, Collection)
    assert FundingRounds._name == 'funding_rounds'


def test_funding_round_cards():
    assert issubclass(FundingRoundCards, BaseCards)
    assert FundingRoundCards.investments == 'investments'
    assert FundingRoundCards.investors == 'investors'
    assert FundingRoundCards.lead_investors == 'lead_investors'
    assert FundingRoundCards.organization == 'organization'
    assert FundingRoundCards.partners == 'partners'
    assert FundingRoundCards.press_references == 'press_references'


def test_funding_round():
    assert issubclass(FundingRound, Entity)
    assert FundingRound.ENTITY_DEF_ID == 'funding_round'
    assert FundingRound.Collection is FundingRounds
    assert FundingRound.Cards is FundingRoundCards
