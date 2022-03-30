from unittest.mock import patch, PropertyMock, MagicMock

import pytest

from src.py_crunchbase.apis.search.predicates import QueryValue, QueryListValue
from src.py_crunchbase.apis.search.query_builder import convert_value, SearchQueryBuilder
from src.py_crunchbase.entities import Entity
from src.py_crunchbase.query_builder import BaseQueryBuilder


class SampleEntity(Entity):
    pass


def test_convert_value():
    av = QueryValue('a')
    assert convert_value(av) == QueryListValue([av])

    with patch('src.py_crunchbase.entities.base.Entity.uuid', new_callable=PropertyMock, return_value='1234'):
        entity = SampleEntity({})
        assert convert_value(entity) == QueryListValue([QueryValue('1234')])

    assert convert_value('45') == QueryListValue([QueryValue('45')])


class TestSearchQueryBuilder:

    @pytest.fixture(name='qb')
    def qb_instance(self):
        return SearchQueryBuilder(SampleEntity)

    def test_constants(self):
        assert issubclass(SearchQueryBuilder, BaseQueryBuilder)

    def test_init(self):
        with patch('src.py_crunchbase.query_builder.BaseQueryBuilder.__init__') as super_init:
            qb = SearchQueryBuilder(SampleEntity, 'a', b='b')
            assert qb.entity_cls is SampleEntity
            assert qb.queries == []
            super_init.assert_called_once_with('a', b='b')

    def test_add_fields(self, qb):
        qb.fields = ['a', 'b']
        with patch.object(qb, 'validate_fields') as validate_fields:
            qb.add_fields(['b', 'c'])
            assert sorted(qb.fields) == ['a', 'b', 'c']
            validate_fields.assert_called_once_with(['b', 'c'])

    def test_validate_fields(self, qb):
        with pytest.raises(qb.Exception, match='Field names cannot be empty'):
            qb.validate_fields([])
        qb.validate_fields(['a'])

    def test_add_query(self, qb):
        with pytest.raises(qb.Exception, match='Field and Operator should be provided in filed__operator format.'):
            qb.add_query('name_opr', 'test')

        with patch('src.py_crunchbase.apis.search.query_builder.OPERATORS', ['eq']):
            with pytest.raises(qb.Exception, match='Invalid operator: neq'):
                qb.add_query('name__neq', 'jojo')

            with patch('src.py_crunchbase.apis.search.query_builder.convert_value', return_value='cv') as _convert_value:
                qb.add_query('name__eq', 'jojo')
                assert qb.queries == [('name', 'eq', 'cv')]
                _convert_value.assert_called_once_with('jojo')

    def test_build(self, qb):
        _super = MagicMock(**{'build.return_value': {'a': 'b'}})
        with patch('src.py_crunchbase.apis.search.query_builder.super', return_value=_super):
            assert qb.build() == {'a': 'b'}

            qb.fields = ['c', 'd']
            assert qb.build() == {'a': 'b', 'field_ids': ['c', 'd']}

            qb.order = [('f', 'asc')]
            assert qb.build() == {'a': 'b', 'field_ids': ['c', 'd'], 'order': [{'field_id': 'f', 'sort': 'asc'}]}

            qb.queries = [
                ('f1', 'op1', MagicMock(**{'evaluate.return_value': ['v1']})),
                ('f2', 'op2', MagicMock(**{'evaluate.return_value': ['v2']}))
            ]
            assert qb.build() == {
                'a': 'b', 'field_ids': ['c', 'd'], 'order': [{'field_id': 'f', 'sort': 'asc'}],
                'query': [
                    {'type': 'predicate', 'field_id': 'f1', 'operator_id': 'op1', 'values': ['v1']},
                    {'type': 'predicate', 'field_id': 'f2', 'operator_id': 'op2', 'values': ['v2']},
                ]
            }
