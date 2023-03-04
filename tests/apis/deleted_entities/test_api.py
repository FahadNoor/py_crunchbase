from unittest.mock import patch, MagicMock

import pytest

from py_crunchbase.apis import CrunchbaseAPI
from py_crunchbase.apis.deleted_entities.api import QueryBuilder, DeletedEntitiesAPI
from py_crunchbase.paginator import Paginated
from py_crunchbase.query_builder import BaseQueryBuilder
from py_crunchbase.utils import DataDict, url_join


class TestQueryBuilder:

    def test_constants(self):
        assert issubclass(QueryBuilder, BaseQueryBuilder)

    def test_build(self):
        qb = QueryBuilder()
        params = {'a': 'b'}
        with patch('py_crunchbase.query_builder.BaseQueryBuilder.build', return_value=params):
            assert qb.build() == {'a': 'b'}

            qb.fields = ['c1', 'c2']
            assert qb.build() == {'a': 'b', 'collection_ids': 'c1,c2'}

            qb.order = [('', 'desc')]
            assert qb.build() == {'a': 'b', 'collection_ids': 'c1,c2', 'deleted_at_order': 'desc'}


class TestDeletedEntitiesAPI:

    @pytest.fixture(name='api', scope='class')
    def api_instance(self):
        return DeletedEntitiesAPI('key')

    def test_constants(self):
        assert issubclass(DeletedEntitiesAPI, (CrunchbaseAPI, Paginated))
        assert DeletedEntitiesAPI.AUTOCOMPLETE_PATH == 'deleted_entities'
        assert DeletedEntitiesAPI.MAX_LIMIT == 1000
        assert DeletedEntitiesAPI.query_builder_cls is QueryBuilder

    def test_init(self):
        qb = MagicMock()
        with patch('py_crunchbase.apis.CrunchbaseAPI.__init__') as super_init:
            with patch.object(DeletedEntitiesAPI, 'query_builder_cls', return_value=qb) as qb_cls:
                api = DeletedEntitiesAPI(api_key='de_api_key')
                super_init.assert_called_once_with(api_key='de_api_key')
                assert api.query_builder is qb
                qb_cls.assert_called_once_with(max_limit=api.MAX_LIMIT)
                assert api.collection_ids == []

                super_init.reset_mock()
                DeletedEntitiesAPI()
                super_init.assert_called_once_with(api_key=None)

    def test__get_path(self, api):
        assert api._get_path() is api.AUTOCOMPLETE_PATH

        api.collection_ids.append('c1')
        assert api._get_path() == url_join(api.AUTOCOMPLETE_PATH, 'c1')

        api.collection_ids.append('c2')
        assert api._get_path() is api.AUTOCOMPLETE_PATH

    def test_select_collections(self, api):
        api.collection_ids = ['1', 'a']
        with patch.object(api.query_builder, 'add_fields') as add_fields:
            return_value = api.select_collections(1, 'b')
            assert return_value is api
            assert isinstance(api.collection_ids, list)
            assert sorted(api.collection_ids) == ['1', 'a', 'b']
            add_fields.assert_called_once_with({'1', 'b'})

    def test_limit(self, api):
        with patch.object(api.query_builder, 'add_limit') as add_limit:
            return_value = api.limit(6)
            assert return_value is api
            add_limit.assert_called_once_with(6)

    def test_order_by_deleted_at(self, api):
        with patch.object(api.query_builder, 'add_order') as add_order:
            return_value = api.order_by_deleted_at()
            assert return_value is api
            add_order.assert_called_once_with('', 'asc')

            add_order.reset_mock()
            api.order_by_deleted_at('desc')
            add_order.assert_called_once_with('', 'desc')

    def test_set_next(self, api):
        data_list = [MagicMock(uuid='12'), MagicMock(uuid='34')]
        with patch.object(api.query_builder, 'add_next') as add_next:
            api.set_next(data_list)
            add_next.assert_called_once_with('34')

    def test_set_previous(self, api):
        data_list = [MagicMock(uuid='12'), MagicMock(uuid='34')]
        with patch.object(api.query_builder, 'add_previous') as add_previous:
            api.set_previous(data_list)
            add_previous.assert_called_once_with('12')

    def test_execute(self, api):
        with patch.object(api, 'send_request', return_value=[{'a': 'b'}, {'c': 'd'}]) as send_request:
            with patch.object(api, '_get_path', return_value='path'):
                with patch.object(api.query_builder, 'build', return_value={'params': 'value'}):
                    assert api.execute() == [DataDict({'a': 'b'}), DataDict({'c': 'd'})]
                    send_request.assert_called_once_with('path', params={'params': 'value'})
