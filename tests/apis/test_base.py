import json
import os
import re
from unittest.mock import MagicMock, patch

import pytest
import requests

from py_crunchbase import constants, CrunchbaseAPIException
from py_crunchbase.apis import CrunchbaseAPI
from py_crunchbase.apis.base import extract_error_info


def complete_url(api: CrunchbaseAPI, path: str) -> str:
    return os.path.join(api.API_URL, api.API_VERSION, path)


class MockedResponse:

    def __init__(self, ok: bool=True, data: dict=None, raising: bool=False):
        self.ok = ok
        self.data = data or {'a': 'b'}
        self.raising = raising

    def json(self):
        if self.raising:
            raise json.JSONDecodeError('decode error', MagicMock(), MagicMock())
        return self.data


def test_extract_error_info():
    data = {}
    assert extract_error_info(data) == ''
    data = {'code': 22, 'error': 'wrong payload'}
    assert extract_error_info(data) == '22: wrong payload'
    data['message'] = 'something not right'
    assert extract_error_info(data) == '22: wrong payload something not right'

    data_2 = {'code': 23, 'error': 'wrong api key'}
    assert extract_error_info([data, data_2]) == '22: wrong payload something not right. 23: wrong api key'


class TestCrunchbaseAPI:

    def test_constants(self):
        assert CrunchbaseAPI.API_URL == constants.CB_API_URL
        assert CrunchbaseAPI.API_VERSION == constants.CB_API_VERSION
        assert CrunchbaseAPI.Exception == CrunchbaseAPIException
        assert CrunchbaseAPI.API_KEY_ENV_VAR == 'PY_CRUNCHBASE_API_KEY'

    def test_init(self, monkeypatch):
        monkeypatch.setenv(CrunchbaseAPI.API_KEY_ENV_VAR, 'api_key_value')
        api = CrunchbaseAPI()
        assert api.api_key == 'api_key_value'
        api = CrunchbaseAPI('new_api_key')
        assert api.api_key == 'new_api_key'

        monkeypatch.delenv(CrunchbaseAPI.API_KEY_ENV_VAR)
        with pytest.raises(
            api.Exception,
            match=f'Please provide an API key at initialization or set an env variable at {api.API_KEY_ENV_VAR}'
        ):
            CrunchbaseAPI()

    def test_send_request(self):
        api = CrunchbaseAPI('api_key')
        url = complete_url(api, 'a_path')
        with patch.object(requests, 'get', return_value=MockedResponse()) as get:
            assert api.send_request('a_path') == {'a': 'b'}
            get.assert_called_once_with(url, params=None, json=None, headers={'X-cb-user-key': api.api_key})

    def test_send_request_post(self):
        api = CrunchbaseAPI('api_key')
        url = complete_url(api, 'b_path')
        with patch.object(requests, 'post', return_value=MockedResponse(data={'c': 'd'})) as post:
            data = api.send_request('b_path', method_name='post', payload={'pay': 'load'}, params={'pa': 'rams'})
            assert data == {'c': 'd'}
            post.assert_called_once_with(
                url, params={'pa': 'rams'}, json={'pay': 'load'}, headers={'X-cb-user-key': api.api_key}
            )

    def test_send_request_exception(self):
        api = CrunchbaseAPI('api_key')
        with patch.object(requests, 'get', side_effect=requests.RequestException('something wrong')):
            with pytest.raises(api.Exception, match='something wrong'):
                api.send_request('a_path')

    def test_send_request_json_exception(self):
        api = CrunchbaseAPI('api_key')
        with patch.object(requests, 'get', return_value=MockedResponse(raising=True)):
            with pytest.raises(api.Exception, match=re.escape('decode error: line 1 column 1 (char 1)')):
                api.send_request('a_path')

    def test_send_request_not_ok(self):
        api = CrunchbaseAPI('api_key')
        with patch.object(requests, 'get', return_value=MockedResponse(ok=False, data={'not': 'ok'})):
            with patch('py_crunchbase.apis.base.extract_error_info', return_value='problem') as extra_info:
                with pytest.raises(api.Exception, match='problem'):
                    api.send_request('a_path')
        extra_info.assert_called_once_with({'not': 'ok'})
