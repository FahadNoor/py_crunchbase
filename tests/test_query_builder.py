from unittest.mock import patch

import pytest

from py_crunchbase import CrunchbaseAPIException
from py_crunchbase.query_builder import BaseQueryBuilder


class TestBaseQueryBuilder:

    @pytest.fixture(name='qb')
    def qb_ins(self):
        return BaseQueryBuilder(min_limit=1, max_limit=5)

    def test_constants(self):
        assert BaseQueryBuilder.Exception is CrunchbaseAPIException

    def test_init(self):
        qb = BaseQueryBuilder()
        assert qb.fields == []
        assert qb.order == []
        assert qb.limit is None
        assert qb.min_limit == 1
        assert qb.max_limit is None
        assert qb.next_id is None
        assert qb.previous_id is None

        qb = BaseQueryBuilder(min_limit=2, max_limit=5)
        assert qb.min_limit == 2
        assert qb.max_limit == 5

    def test_add_fields(self, qb):
        qb.fields = ['a']
        with patch.object(qb, 'validate_fields') as validate_fields:
            qb.add_fields(['a', 'b'])
            validate_fields.assert_called_once_with(['a', 'b'])
            assert sorted(qb.fields) == ['a', 'b']

    def test_add_order(self, qb):
        qb.add_order('f', 'desc')
        assert qb.order == [('f', 'desc')]

    def test_add_limit(self, qb):
        qb.add_limit(3)
        assert qb.limit == 3
        qb.add_limit(0)
        assert qb.limit == 1
        qb.add_limit(6)
        assert qb.limit == 5

    def test_add_next(self, qb):
        qb.next_id = 'a'
        qb.previous_id = 'b'
        qb.add_next('c')
        assert qb.previous_id is None
        assert qb.next_id == 'c'

    def test_add_previous(self, qb):
        qb.next_id = 'a'
        qb.previous_id = 'b'
        qb.add_previous('c')
        assert qb.next_id is None
        assert qb.previous_id == 'c'

    def test_build(self, qb):
        assert qb.build() == {}
        qb.next_id = 'a'
        assert qb.build() == {'after_id': 'a'}
        qb.previous_id = 'b'
        assert qb.build() == {'after_id': 'a', 'before_id': 'b'}
        qb.limit = 5
        assert qb.build() == {'after_id': 'a', 'before_id': 'b', 'limit': 5}
