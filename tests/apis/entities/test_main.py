from unittest.mock import patch, MagicMock

import pytest

from src.py_crunchbase.apis.entities.main import EntitiesAPIProxy
from src.py_crunchbase.entities import Entity


class SampleEntity(Entity):
    pass


class TestEntitiesAPIProxy:

    @pytest.fixture(name='api', scope='class')
    def api_instance(self):
        return EntitiesAPIProxy(entity_cls=SampleEntity, api_key='e_api_p_key')

    def test_init(self):
        api = EntitiesAPIProxy(entity_cls=SampleEntity, api_key='e_api_p_key')
        assert api.entity_cls is SampleEntity
        assert api.api_key == 'e_api_p_key'

        api = EntitiesAPIProxy(entity_cls=SampleEntity)
        assert api.api_key is None

    def test_get(self, api):
        entity = MagicMock()
        entities_api = MagicMock(**{'execute.return_value': entity})
        with patch.object(api, 'get_entities_api', return_value=entities_api) as get_entities_api:
            assert api.get('12') is entity
            get_entities_api.assert_called_once_with('12')
            entities_api.select_all.assert_called_once()

            get_entities_api.reset_mock()
            assert api.get('23', field_ids=['f1', 'f2', 'f2'], card_ids=['c1', 'c2', 'c1']) is entity
            get_entities_api.assert_called_once_with('23')
            assert sorted(entities_api.select.call_args.args) == ['f1', 'f2']
            assert sorted(entities_api.select_cards.call_args.args) == ['c1', 'c2']

    def test_get_cards(self, api):
        entities_api = MagicMock(**{'iterate.return_value': [
            MagicMock(cards={'id': [{'1st': '1st_v'}, {'2nd': '2nd_v'}]}),
            MagicMock(cards={'id': [{'3rd': '3rd_v'}, {'4th': '4th_v'}]}),
        ]})
        with patch.object(api, 'get_cards_api', return_value=entities_api) as get_cards_api:
            assert api.get_cards(entity_id='1', card_id='2') == [
                {'1st': '1st_v'}, {'2nd': '2nd_v'}, {'3rd': '3rd_v'}, {'4th': '4th_v'}
            ]
            get_cards_api.assert_called_once_with(entity_id='1', card_id='2')

            api.get_cards(entity_id='2', card_id='4', card_field_ids=['c1', 'c2', 'c2'], order_by='f_name')
            entities_api.select.assert_called_once()
            assert sorted(entities_api.select.call_args.args) == ['c1', 'c2']
            entities_api.order_by.assert_called_once_with('f_name')

            entities_api.order_by.reset_mock()
            api.get_cards(entity_id='2', card_id='4', order_by=('f_n', 'desc'))
            entities_api.order_by.assert_called_once_with('f_n', 'desc')

    def test_get_entities_api(self, api):
        entities_api = MagicMock()
        with patch('src.py_crunchbase.apis.entities.main.EntitiesAPI', return_value=entities_api) as EntitiesAPI:
            assert api.get_entities_api('1') is entities_api
            EntitiesAPI.assert_called_once_with(entity_id='1', entity_cls=api.entity_cls, api_key=api.api_key)

    def test_get_cards_api(self, api):
        cards_api = MagicMock()
        with patch('src.py_crunchbase.apis.entities.main.CardsAPI', return_value=cards_api) as CardsAPI:
            assert api.get_cards_api(entity_id='1', card_id='2') is cards_api
            CardsAPI.assert_called_once_with(entity_id='1', card_id='2', entity_cls=api.entity_cls, api_key=api.api_key)
