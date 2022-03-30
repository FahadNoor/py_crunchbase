from unittest.mock import patch, MagicMock, call

import pytest

from src.py_crunchbase import Entities
from src.py_crunchbase.apis import AutoCompleteAPI, CrunchbaseAPI


class TestAutoCompleteAPI:

    def test_constants(self):
        assert AutoCompleteAPI.AUTOCOMPLETE_PATH == 'autocompletes'
        assert AutoCompleteAPI.MAX_LIMIT == 25
        assert issubclass(AutoCompleteAPI, CrunchbaseAPI)

    def test_init(self):
        with patch('src.py_crunchbase.apis.CrunchbaseAPI.__init__') as super_init:
            api = AutoCompleteAPI('key_value')
        super_init.assert_called_once_with(api_key='key_value')
        assert api.query is None
        assert api.collection_ids == []
        assert api.limit_value == api.MAX_LIMIT

        with patch('src.py_crunchbase.apis.CrunchbaseAPI.__init__') as super_init:
            AutoCompleteAPI()
        super_init.assert_called_once_with(api_key=None)

    def test_autocomplete(self):
        api = AutoCompleteAPI('key')
        return_value = api.autocomplete('sample_query')
        assert api.query == 'sample_query'
        assert return_value is api

    def test_select_collections(self):
        api = AutoCompleteAPI('key')
        api.collection_ids = ['a', 'c', 'd']
        return_value = api.select_collections('a', 'e', 'x')
        assert isinstance(api.collection_ids, list)
        assert sorted(api.collection_ids) == ['a', 'c', 'd', 'e', 'x']
        assert return_value is api

    def test_limit(self):
        api = AutoCompleteAPI('key')
        return_value = api.limit(4)
        assert api.limit_value == 4
        assert return_value is api

    def test_execute(self):
        api = AutoCompleteAPI('key')
        api.query = 'a_query'

        ent_a, ent_b = MagicMock(), MagicMock()
        result = {'entities': ['data_a', 'data_b']}
        with patch.object(api, 'send_request', return_value=result) as send_request:
            with patch.object(Entities, 'dict_to_entity', side_effect=[ent_a, ent_b]) as dict_to_entity:
                assert api.execute() == [ent_a, ent_b]

        send_request.assert_called_once_with(api.AUTOCOMPLETE_PATH, params={'query': 'a_query', 'limit': api.MAX_LIMIT})
        dict_to_entity.assert_has_calls([call('data_a'), call('data_b')])

    def test_execute_optionals(self):
        api = AutoCompleteAPI('key')
        api.query = 'a_query'
        api.collection_ids = ['c_1', 'c_2']
        api.limit_value = 3

        ent_a, ent_b = MagicMock(), MagicMock()
        result = {'entities': ['data_a', 'data_b']}
        with patch.object(api, 'send_request', return_value=result) as send_request:
            with patch.object(Entities, 'dict_to_entity', side_effect=[ent_a, ent_b]) as dict_to_entity:
                assert api.execute() == [ent_a, ent_b]

                send_request.assert_called_once_with(
                    api.AUTOCOMPLETE_PATH, params={'query': 'a_query', 'collection_ids': 'c_1,c_2', 'limit': 3}
                )
                dict_to_entity.assert_has_calls([call('data_a'), call('data_b')])

                # test max limit check
                send_request.reset_mock()
                dict_to_entity.side_effect = [ent_a, ent_b]
                api.limit(api.MAX_LIMIT + 1)
                api.execute()
                send_request.assert_called_once_with(
                    api.AUTOCOMPLETE_PATH,
                    params={'query': 'a_query', 'collection_ids': 'c_1,c_2', 'limit': api.MAX_LIMIT}
                )

    def test_execute_exc(self):
        api = AutoCompleteAPI('key')
        with pytest.raises(ValueError, match='None is not a valid query'):
            api.execute()
