from unittest.mock import MagicMock, patch

from src.py_crunchbase.apis.search.predicates import OPERATORS, QueryValue, QueryListValue, Currency


def test_operators():
    assert OPERATORS == {
        'eq', 'contains', 'not_includes', 'lte', 'starts', 'domain_eq', 'gt', 'not_contains', 'not_eq', 'between',
        'gte', 'not_includes_all', 'includes', 'includes_all', 'blank', 'lt'
    }


class TestQueryValue:

    def test_init(self):
        qv = QueryValue('a_value')
        assert qv.value == 'a_value'

    def test_evaluate(self):
        qv = QueryValue('a_value')
        assert qv.evaluate() == qv.value


class TestQueryListValue:

    def test_constants(self):
        assert issubclass(QueryListValue, QueryValue)

    def test_evaluate(self):
        values = [MagicMock(**{'evaluate.return_value': 'a'}), MagicMock(**{'evaluate.return_value': 'b'})]
        qv = QueryListValue(values)
        assert qv.evaluate() == ['a', 'b']


class TestCurrency:

    def test_constants(self):
        assert issubclass(Currency, QueryValue)

    def test_init(self):
        with patch('src.py_crunchbase.apis.search.predicates.QueryValue.__init__') as super_init:
            cur = Currency(2)
            super_init.assert_called_once_with(2)
            assert cur.currency == 'USD'

            cur = Currency(2, currency='PKR')
            assert cur.currency == 'PKR'

    def test_evaluate(self):
        cur = Currency(2)
        assert cur.evaluate() == {'value': cur.value, 'currency': cur.currency}
