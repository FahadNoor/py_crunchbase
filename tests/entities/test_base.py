import os.path
from unittest.mock import patch

import pytest

from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.utils import DataDict


class DogCollection(Collection):

    _name = 'GoodBoys'
    _facet_name = 'Goodboy'

    Retriever = 'retriever'
    Shepherd = 'shepherd'


class CatCards(BaseCards):

    sheru = 'sheru'
    bebo = 'bebo'


def test_collection():

    assert DogCollection.Retriever == 'Goodboy.retriever'
    assert DogCollection.Shepherd == 'Goodboy.shepherd'
    assert str(DogCollection) == 'GoodBoys'


def test_base_cards():
    assert CatCards.all() == ('bebo', 'fields', 'sheru')


class TestEntity:

    @pytest.fixture(name='entity', scope='class')
    def get_entity(self):
        return Entity(
            {'identifier': {'uuid': '12', 'permalink': 'a_link', 'entity_def_id': 'id'}}
        )

    def test_constants(self):
        assert issubclass(Entity, DataDict)
        assert Entity.ENTITY_DEF_ID == ''
        assert Entity.Collection is None
        assert Entity.Cards is None
        assert Entity.Facets is None

    def test_init(self):
        with patch('src.py_crunchbase.utils.DataDict.__init__') as super_init:
            data = {'a': 'A', 'b': 'B'}
            entity = Entity(data)
            assert entity._original_entity_data is not data
            assert entity._original_entity_data == data
            assert entity.cards is None
            super_init.assert_called_once_with(data)

    def test_uuid(self, entity):
        assert entity.uuid == '12'
        assert Entity({}).uuid == ''

    def test_permalink(self, entity):
        assert entity.permalink == 'a_link'
        assert Entity({}).permalink == ''

    def test_entity_def_id(self, entity):
        with patch.object(entity, 'ENTITY_DEF_ID', 'some_id'):
            assert entity.entity_def_id == 'some_id'
        assert entity.entity_def_id == 'id'
        assert Entity({}).entity_def_id == ''

    def test_web_url(self, entity):
        with patch('src.py_crunchbase.entities.base.CB_WEBSITE_URL', 'cb_url'):
            assert entity.web_url == os.path.join('cb_url', entity.entity_def_id, entity.permalink)

    def test_api_path(self):
        with patch.object(Entity, 'Collection', 1):
            assert Entity.api_path() == '1'
