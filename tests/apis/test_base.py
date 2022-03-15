from py_crunchbase import constants, CrunchbaseAPIException
from py_crunchbase.apis import CrunchbaseAPI


class TestCrunchbaseAPI:

    def test_constants(self):
        assert CrunchbaseAPI.API_URL == constants.CB_API_URL
        assert CrunchbaseAPI.API_VERSION == constants.CB_API_VERSION
        assert CrunchbaseAPI.Exception == CrunchbaseAPIException
        assert CrunchbaseAPI.API_KEY_ENV_VAR == 'PY_CRUNCHBASE_API_KEY'
