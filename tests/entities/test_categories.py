from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.categories import Categories, CategoryCards, Category


def test_categories():
    assert issubclass(Categories, Collection)
    assert Categories._name == 'categories'


def test_category_cards():
    assert issubclass(CategoryCards, BaseCards)


def test_category():
    assert issubclass(Category, Entity)
    assert Category.ENTITY_DEF_ID == 'category'
    assert Category.Collection is Categories
    assert Category.Cards is CategoryCards
