import random
from unittest.mock import patch, MagicMock

import pytest

from py_crunchbase import PyCrunchbase
from py_crunchbase.entities import Entity, Entities


class SampleEntity(Entity):
    pass


class TestPyCrunchbase:

    @pytest.fixture(name='api', scope='class')
    def api_instance(self):
        return PyCrunchbase('key')

    def test_init(self):
        api = PyCrunchbase('key')
        assert api.api_key == 'key'

        api = PyCrunchbase()
        assert api.api_key is None

    def test_autocomplete_api(self, api):
        ac_api = MagicMock()
        with patch('py_crunchbase.main.AutoCompleteAPI', return_value=ac_api) as AutoCompleteAPI:
            assert api.autocomplete_api() == ac_api
            AutoCompleteAPI.assert_called_once_with(api_key=api.api_key)

    def test_deleted_entities_api(self, api):
        de_api = MagicMock()
        with patch('py_crunchbase.main.DeletedEntitiesAPI', return_value=de_api) as DeletedEntitiesAPI:
            assert api.deleted_entities_api() == de_api
            DeletedEntitiesAPI.assert_called_once_with(api_key=api.api_key)

    def test__entities_api(self, api):
        e_api = MagicMock()
        with patch('py_crunchbase.main.EntitiesAPI', return_value=e_api) as EntitiesAPI:
            assert api._entities_api(SampleEntity) == e_api
            EntitiesAPI.assert_called_once_with(SampleEntity, api_key=api.api_key)

    def test_all_entities_methods(self, api):
        method_initials = (
            'acquisitions', 'addresses', 'categories', 'category_groups', 'degrees', 'event_appearances', 'events',
            'funding_rounds', 'funds', 'investments', 'ipos', 'jobs', 'locations', 'organizations', 'ownerships',
            'people', 'press_references'
        )

        entity_classes = (
            Entities.Acquisition, Entities.Address, Entities.Category, Entities.CategoryGroup, Entities.Degree,
            Entities.EventAppearance, Entities.Event, Entities.FundingRound, Entities.Fund, Entities.Investment,
            Entities.Ipo, Entities.Job, Entities.Location, Entities.Organization, Entities.Ownership, Entities.Person,
            Entities.PressReference
        )

        for method_initial, entity_cls in zip(method_initials, entity_classes):
            method = getattr(api, f'{method_initial}_api')
            return_value = random.randint(1, 1000)
            with patch.object(api, '_entities_api', return_value=return_value) as _entities_api:
                assert method() == return_value
                _entities_api.assert_called_once_with(entity_cls)

    def test__search_api(self, api):
        s_api = MagicMock()
        with patch('py_crunchbase.main.SearchAPI', return_value=s_api) as SearchAPI:
            assert api._search_api(SampleEntity) == s_api
            SearchAPI.assert_called_once_with(SampleEntity, api_key=api.api_key)

    def test_all_search_methods(self, api):
        method_names = (
            'acquisitions', 'addresses', 'categories', 'category_groups', 'degrees', 'event_appearances', 'events',
            'funding_rounds', 'funds', 'investments', 'ipos', 'jobs', 'key_employee_changes', 'layoffs', 'locations',
            'organizations', 'ownerships', 'people', 'press_references', 'principals'
        )

        entity_classes = (
            Entities.Acquisition, Entities.Address, Entities.Category, Entities.CategoryGroup, Entities.Degree,
            Entities.EventAppearance, Entities.Event, Entities.FundingRound, Entities.Fund, Entities.Investment,
            Entities.Ipo, Entities.Job, Entities.KeyEmployeeChange, Entities.Layoff, Entities.Location,
            Entities.Organization, Entities.Ownership, Entities.Person, Entities.PressReference, Entities.Principal
        )

        for method_name, entity_cls in zip(method_names, entity_classes):
            method = getattr(api, f'search_{method_name}_api')
            return_value = random.randint(1, 1000)
            with patch.object(api, '_search_api', return_value=return_value) as _search_api:
                assert method() == return_value
                _search_api.assert_called_once_with(entity_cls)
