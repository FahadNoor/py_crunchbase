from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.funds import Funds, FundCards, Fund


def test_funds():
    assert issubclass(Funds, Collection)
    assert Funds._name == 'funds'


def test_fund_cards():
    assert issubclass(FundCards, BaseCards)
    assert FundCards.investors == 'investors'
    assert FundCards.owner == 'owner'
    assert FundCards.press_references == 'press_references'


def test_fund():
    assert issubclass(Fund, Entity)
    assert Fund.ENTITY_DEF_ID == 'fund'
    assert Fund.Collection is Funds
    assert Fund.Cards is FundCards
