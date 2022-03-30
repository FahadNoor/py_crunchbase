import os.path
from unittest.mock import patch, call

import pytest

from src.py_crunchbase import Entities
from src.py_crunchbase.apis import CrunchbaseAPI
from src.py_crunchbase.apis.entities.base_ import parse_cards, BaseEntitiesAPI
from src.py_crunchbase.entities import Entity, BaseCards
from src.py_crunchbase.utils import DataDict


class SampleEntity(Entity):

    ENTITY_DEF_ID = 'sample_def_id'


def test_parse_cards():
    cards = {
        'a': [{'uuid': '1'}, {'uuid': '2'}],
        'b': [{'uuid': '3'}, {'uuid': '4'}],
    }
    data = [{'f': '1'}, {'f': '2'}, {'f': '3'}, {'f': '4'}]
    with patch.object(Entities, 'dict_to_entity', side_effect=data) as dict_to_entity:
        assert parse_cards(cards) == DataDict({
            'a': [{'f': '1'}, {'f': '2'}],
            'b': [{'f': '3'}, {'f': '4'}],
        })
        dict_to_entity.assert_has_calls([
            call({'uuid': '1'}), call({'uuid': '2'}), call({'uuid': '3'}), call({'uuid': '4'})
        ])


class TestBaseEntitiesAPI:

    @pytest.fixture(name='entity')
    def entity_instance(self):
        return SampleEntity({'identifier': {'uuid': '1234', 'permalink': 'link'}})

    @pytest.fixture(name='api', scope='class')
    def api_instance(self):
        return BaseEntitiesAPI(entity_cls=SampleEntity, api_key='key')

    def test_constants(self):
        assert issubclass(BaseEntitiesAPI, CrunchbaseAPI)
        assert BaseEntitiesAPI.ENTITIES_PATH == 'entities'
        assert BaseEntitiesAPI.CARDS_PATH == 'cards'

    def test_init(self):
        with patch('src.py_crunchbase.apis.CrunchbaseAPI.__init__') as super_init:
            api = BaseEntitiesAPI(entity_cls=Entity, api_key='be_api_key')
            super_init.assert_called_once_with(api_key='be_api_key')
            assert api.entity_cls is Entity

            super_init.reset_mock()
            BaseEntitiesAPI(entity_cls=Entity)
            super_init.assert_called_once_with(api_key=None)

    def test__get_entity_id(self, entity, api):
        AnotherSampleEntity = type('AnotherSampleEntity', (Entity,), {})
        assert api._get_entity_id('5678') == '5678'
        with pytest.raises(api.Exception, match='Entity should be an instance of SampleEntity'):
            api._get_entity_id(AnotherSampleEntity({}))
        assert api._get_entity_id(entity) == '1234'
        entity['identifier'].pop('uuid')
        assert api._get_entity_id(entity) == 'link'
        entity['identifier'].pop('permalink')
        assert api._get_entity_id(entity) == ''

    def test__get_path(self, api):
        with patch.object(SampleEntity, 'api_path', return_value='sample_path'):
            path = os.path.join(api.ENTITIES_PATH, 'sample_path', 'e1')
            assert api._get_path('e1') == path
            assert api._get_path('e1', 'c1') == os.path.join(path, api.CARDS_PATH, 'c1')

    def test__parse_response_data(self, api):
        entity_data = {'identifier': {'uuid': 'apple'}}
        data = {'cards': {BaseCards.fields: entity_data, 'card_1': ['a'], 'card_2': ['b']}}
        with patch('src.py_crunchbase.apis.entities.base_.parse_cards', return_value={'cards': 'list'}) as _parse_cards:
            entity = api._parse_response_data(data)
        assert isinstance(entity, SampleEntity)
        assert dict(entity) == entity_data
        assert entity.cards == {'cards': 'list'}

        _parse_cards.assert_called_once_with({'card_1': ['a'], 'card_2': ['b']})

        data = {'properties': {'prop': '1'}}
        entity = api._parse_response_data(data)
        assert dict(entity) == {'prop': '1'}
