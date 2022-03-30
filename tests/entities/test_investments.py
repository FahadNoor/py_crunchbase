from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.investments import Investments, InvestmentCards, Investment


def test_investments():
    assert issubclass(Investments, Collection)
    assert Investments._name == 'investments'


def test_investment_cards():
    assert issubclass(InvestmentCards, BaseCards)
    assert InvestmentCards.funding_round == 'funding_round'
    assert InvestmentCards.investor == 'investor'
    assert InvestmentCards.organization == 'organization'
    assert InvestmentCards.partner == 'partner'


def test_investment():
    assert issubclass(Investment, Entity)
    assert Investment.ENTITY_DEF_ID == 'investment'
    assert Investment.Collection is Investments
    assert Investment.Cards is InvestmentCards
