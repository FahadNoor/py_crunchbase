import json
import os
from typing import Union

import requests


class CrunchbaseAPIException(Exception):
    pass


def extract_error_info(data) -> str:
    data_list = data if isinstance(data, list) else [data]
    msgs = []
    for data in data_list:
        msg = ''
        if 'code' in data:
            msg += f"{data['code']}: "
        if 'error' in data:
            msg += data['error']
        if 'message' in data:
            msg += f" {data['message']}"
        msgs.append(msg)
    return '. '.join(msgs)


class CrunchbaseAPI:

    API_URL = 'https://api.crunchbase.com/api'
    API_VERSION = 'v4'
    Exception = CrunchbaseAPIException
    API_KEY_ENV_VAR = 'PY_CRUNCHBASE_API_KEY'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv(self.API_KEY_ENV_VAR)
        if not self.api_key:
            raise self.Exception(
                f'Please provide an API key at initialization or set an env variable at {self.API_KEY_ENV_VAR}'
            )

    def send_request(
            self, path: str, method_name: str = 'get', payload: dict = None, params: dict = None
    ) -> Union[dict, list]:
        """
        helper method to send an API request
        :returns response dict/list or raises an exception
        """
        url = os.path.join(self.API_URL, self.API_VERSION, path)
        method = getattr(requests, method_name, requests.get)

        response = method(url, params=params, json=payload, headers={'X-cb-user-key': self.api_key})
        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            raise self.Exception(str(exc)) from exc

        if response.ok:
            return data

        raise self.Exception(extract_error_info(data) or response.reason)


__all__ = ['CrunchbaseAPIException', 'CrunchbaseAPI']
