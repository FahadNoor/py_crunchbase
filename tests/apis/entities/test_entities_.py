from unittest.mock import patch, PropertyMock

import pytest

from src.py_crunchbase.apis.entities.base_ import BaseEntitiesAPI
from src.py_crunchbase.apis.entities.entities_ import EntitiesAPI
from src.py_crunchbase.entities import Entity, BaseCards


class SampleEntity(Entity):
    pass


class TestEntitiesAPI:

    @pytest.fixture(name='api')
    def api_instance(self):
        return EntitiesAPI(entity_id='1', entity_cls=SampleEntity, api_key='e_api_key')

    def test_constants(self):
        assert issubclass(EntitiesAPI, BaseEntitiesAPI)
        assert EntitiesAPI.ALL_FIELDS == '__ALL__'

    def test_init(self):
        with patch('src.py_crunchbase.apis.entities.base_.BaseEntitiesAPI.__init__') as super_init:
            with patch.object(EntitiesAPI, '_get_entity_id', return_value='2') as _get_entity_id:
                api = EntitiesAPI(entity_id='1', entity_cls=SampleEntity, api_key='e_api_key')
                super_init.assert_called_once_with(entity_cls=SampleEntity, api_key='e_api_key')
                assert api.entity_id == '2'
                assert api.field_ids == []
                assert api.card_ids == []

                super_init.reset_mock()
                EntitiesAPI(entity_id='1', entity_cls=SampleEntity)
                super_init.assert_called_once_with(entity_cls=SampleEntity, api_key=None)

    def test_select(self, api):
        api.card_ids.append('c1')
        return_value = api.select(api.ALL_FIELDS)
        assert return_value is api
        assert api.card_ids == ['c1', BaseCards.fields]

        api.select(api.ALL_FIELDS)
        assert api.card_ids == ['c1', BaseCards.fields]

        api.field_ids.append('f1')
        api.select('f1', 'f2')
        assert sorted(api.field_ids) == ['f1', 'f2']

    def test_select_all(self, api):
        with patch.object(api, 'select', return_value=api) as select:
            return_value = api.select_all()
            assert return_value is api
            select.assert_called_once_with(api.ALL_FIELDS)

    def test_select_cards(self, api):
        api.card_ids.append('c1')
        return_value = api.select_cards('c1', 'c2')
        assert return_value is api
        assert sorted(api.card_ids) == ['c1', 'c2']

    def test_select_all_cards(self, api):
        with patch.object(api, 'select_cards') as select_cards:
            return_value = api.select_all_cards()
            assert return_value is api
            select_cards.assert_not_called()

            with patch.object(api.entity_cls, 'Cards', new_callable=PropertyMock, return_value=BaseCards):
                api.select_all_cards()
                select_cards.assert_called_once_with(BaseCards.fields)

    def test_execute(self, api):
        with patch.object(api, '_get_path', return_value='p_value') as _get_path:
            with patch.object(api, 'send_request', return_value={'resp': 'data'}) as send_request:
                with patch.object(api, '_parse_response_data', return_value={'parsed': 'data'}) as _parse_response_data:
                    assert api.execute() == {'parsed': 'data'}

                    _get_path.assert_called_once_with(api.entity_id)
                    send_request.assert_called_once_with('p_value', params=None)
                    _parse_response_data.assert_called_once_with({'resp': 'data'})

                    send_request.reset_mock()
                    api.field_ids = ['f1', 'f2']
                    api.card_ids = ['c1', 'c2']
                    api.execute()
                    send_request.assert_called_once_with('p_value', params={'field_ids': 'f1,f2', 'card_ids': 'c1,c2'})
