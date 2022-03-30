from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.degrees import Degrees, DegreeCards, Degree


def test_degrees():
    assert issubclass(Degrees, Collection)
    assert Degrees._name == 'degrees'


def test_degree_cards():
    assert issubclass(DegreeCards, BaseCards)
    assert DegreeCards.organization == 'organization'
    assert DegreeCards.person == 'person'


def test_degree():
    assert issubclass(Degree, Entity)
    assert Degree.ENTITY_DEF_ID == 'degree'
    assert Degree.Collection is Degrees
    assert Degree.Cards is DegreeCards
