from py_crunchbase.entities import Collection, Entity
from py_crunchbase.entities.layoffs import Layoffs, Layoff


def test_layoffs():
    assert issubclass(Layoffs, Collection)
    assert Layoffs._name == 'layoffs'


def test_layoff():
    assert issubclass(Layoff, Entity)
    assert Layoff.ENTITY_DEF_ID == 'layoff'
    assert Layoff.Collection is Layoffs
