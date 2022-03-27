from unittest.mock import patch, MagicMock, call

import pytest

from py_crunchbase.apis import SearchAPI, CrunchbaseAPI
from py_crunchbase.apis.search.query_builder import SearchQueryBuilder
from py_crunchbase.entities import Entity
from py_crunchbase.paginator import Paginated


class SampleEntity(Entity):
    pass


class TestSearchAPI:

    @pytest.fixture(name='api', scope='class')
    def api_instance(self):
        return SearchAPI(entity_cls=SampleEntity, api_key='s_api_key')

    def test_constants(self):
        assert issubclass(SearchAPI, (CrunchbaseAPI, Paginated))
        assert SearchAPI.query_builder_cls is SearchQueryBuilder
        assert SearchAPI.MAX_LIMIT == 2000

    def test_init(self):
        qb = MagicMock()
        with patch('py_crunchbase.apis.base.CrunchbaseAPI.__init__') as super_init:
            with patch.object(SampleEntity, 'api_path', return_value='sample_path'):
                with patch.object(SearchAPI, 'get_query_builder', return_value=qb):
                    api = SearchAPI(entity_cls=SampleEntity, api_key='s_api_key')
                    super_init.assert_called_once_with(api_key='s_api_key')
                    assert api.path == 'searches/sample_path'
                    assert api.entity_cls is SampleEntity
                    assert api.query_builder is qb

                    super_init.reset_mock()
                    SearchAPI(entity_cls=SampleEntity)
                    super_init.assert_called_once_with(api_key=None)

    def test_reset(self):
        qb = MagicMock()
        api = SearchAPI(entity_cls=SampleEntity, api_key='s_api_key')
        with patch.object(api, 'get_query_builder', return_value=qb):
            api.reset()
            assert api.query_builder is qb

    def test_get_query_builder(self, api):
        with patch.object(api, 'query_builder_cls', return_value='abc') as query_builder_cls:
            assert api.get_query_builder() == 'abc'
            query_builder_cls.assert_called_once_with(api.entity_cls, max_limit=api.MAX_LIMIT)

    def test_select(self, api):
        with patch.object(api.query_builder, 'add_fields') as add_fields:
            return_value = api.select('a', 'b')
            assert return_value is api
            add_fields.assert_called_once_with(('a', 'b'))

    def test_where(self, api):
        with patch.object(api.query_builder, 'add_query') as add_query:
            return_value = api.where(name__equal='gigi', buddy__is='sheru')
            assert return_value is api
            add_query.assert_has_calls([call('name__equal', 'gigi'), call('buddy__is', 'sheru')])

    def test_order_by(self, api):
        with patch.object(api.query_builder, 'add_order') as add_order:
            return_value = api.order_by('a_field')
            assert return_value is api
            add_order.assert_called_once_with('a_field', 'asc')

            add_order.reset_mock()
            api.order_by('b_field', 'desc')
            add_order.assert_called_once_with('b_field', 'desc')

    def test_limit(self, api):
        with patch.object(api.query_builder, 'add_limit') as add_limit:
            return_value = api.limit(5)
            assert return_value is api
            add_limit.assert_called_once_with(5)

    def test_set_next(self, api):
        entities = [MagicMock(uuid='1'), MagicMock(uuid='2')]
        with patch.object(api.query_builder, 'add_next') as add_next:
            api.set_next(entities)
            add_next.assert_called_once_with('2')

    def test_set_previous(self, api):
        entities = [MagicMock(uuid='1'), MagicMock(uuid='2')]
        with patch.object(api.query_builder, 'add_previous') as add_previous:
            api.set_previous(entities)
            add_previous.assert_called_once_with('1')

    def test_execute(self, api):
        data = {'entities': [{'properties': {'a': '1'}}, {'properties': {'a': '2'}}]}
        with patch.object(api.query_builder, 'build', return_value={'pay': 'load'}):
            with patch.object(api, 'send_request', return_value=data) as send_request:
                with patch.object(api, 'entity_cls', side_effect=['e1', 'e2']) as entity_cls:
                    assert api.execute() == ['e1', 'e2']
                    entity_cls.assert_has_calls([call({'a': '1'}), call({'a': '2'})])
                    send_request.assert_called_once_with(api.path, method_name='post', payload={'pay': 'load'})
