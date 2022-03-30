from unittest.mock import MagicMock, patch

import pytest

from src.py_crunchbase.apis.entities.base_ import BaseEntitiesAPI
from src.py_crunchbase.apis.entities.cards import Paginator, QueryBuilder, CardsAPI
from src.py_crunchbase.entities import Entity
from src.py_crunchbase.paginator import Paginator as BasePaginator, Paginated
from src.py_crunchbase.query_builder import BaseQueryBuilder


class SampleEntity(Entity):
    pass


class TestPaginator:

    def test_constants(self):
        assert issubclass(Paginator, BasePaginator)

    def test__next__(self):
        api = MagicMock()
        entity = None
        paginator = Paginator(api)
        with patch.object(paginator, 'next', return_value=entity):
            with pytest.raises(StopIteration):
                paginator.__next__()

        entity = MagicMock(cards=[])
        with patch.object(paginator, 'next', return_value=entity):
            with pytest.raises(StopIteration):
                paginator.__next__()

            entity.cards = ['a']
            assert paginator.__next__() is entity


class TestQueryBuilder:

    def test_constants(self):
        assert issubclass(QueryBuilder, BaseQueryBuilder)

    def test_build(self):
        qb = QueryBuilder()
        params = {'a': 'b'}
        with patch('src.py_crunchbase.query_builder.BaseQueryBuilder.build', return_value=params):
            assert qb.build() == {'a': 'b'}

            qb.order = [('field', 'desc')]
            assert qb.build() == {'a': 'b', 'order': 'field,desc'}

            qb.fields = ['c1', 'c2']
            assert qb.build() == {'a': 'b', 'order': 'field,desc', 'card_field_ids': 'c1,c2'}


class TestCardsAPI:

    @pytest.fixture(name='api', scope='class')
    def get_api(self):
        return CardsAPI(entity_id='2', card_id='3', entity_cls=SampleEntity, api_key='c_api_key')

    def test_constants(self):
        assert issubclass(CardsAPI, (BaseEntitiesAPI, Paginated))
        assert CardsAPI.query_builder_cls is QueryBuilder
        assert CardsAPI.paginator_cls is Paginator
        assert CardsAPI.MAX_LIMIT == 100

    def test_init(self):
        qb = MagicMock()
        entity_cls = SampleEntity
        with patch('src.py_crunchbase.apis.entities.base_.BaseEntitiesAPI.__init__') as super_init:
            with patch.object(CardsAPI, 'query_builder_cls', return_value=qb) as query_builder_cls:
                with patch.object(CardsAPI, '_get_entity_id', return_value='1') as _get_entity_id:
                    api = CardsAPI(entity_id='2', card_id='3', entity_cls=entity_cls, api_key='c_api_key')

                    super_init.assert_called_once_with(entity_cls=entity_cls, api_key='c_api_key')
                    query_builder_cls.assert_called_once_with(max_limit=api.MAX_LIMIT)
                    _get_entity_id.assert_called_once_with('2')
                    assert api.query_builder is qb
                    assert api.entity_id == '1'
                    assert api.card_id == '3'

                    super_init.reset_mock()
                    CardsAPI(entity_id='2', card_id='3', entity_cls=entity_cls)
                    super_init.assert_called_once_with(entity_cls=entity_cls, api_key=None)

    def test_select(self, api):
        with patch.object(api.query_builder, 'add_fields') as add_fields:
            return_value = api.select('a', 'b')
            assert return_value is api
            add_fields.assert_called_once_with(('a', 'b'))

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
        entity = MagicMock(cards={'a': [MagicMock(uuid='1'), MagicMock(uuid='2')]})
        with patch.object(api.query_builder, 'add_next') as add_next:
            api.set_next(entity)
            add_next.assert_called_once_with('2')

    def test_set_previous(self, api):
        entity = MagicMock(cards={'a': [MagicMock(uuid='3'), MagicMock(uuid='4')]})
        with patch.object(api.query_builder, 'add_previous') as add_previous:
            api.set_previous(entity)
            add_previous.assert_called_once_with('3')

    def test_execute(self, api):
        entity = MagicMock()
        with patch.object(api, '_get_path', return_value='path_value') as _get_path:
            with patch.object(api, '_parse_response_data', return_value=entity) as _parse_response_data:
                with patch.object(api, 'send_request', return_value={'data': 'value'}) as send_request:
                    with patch.object(api.query_builder, 'build', return_value={'params': 'value'}) as build:
                        return_value = api.execute()
                        assert return_value is entity
                        _get_path.assert_called_once_with(api.entity_id, api.card_id)
                        build.assert_called_once()
                        send_request.assert_called_once_with('path_value', params={'params': 'value'})
                        _parse_response_data.assert_called_once_with({'data': 'value'})
