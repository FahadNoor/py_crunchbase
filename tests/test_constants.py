from src.py_crunchbase import constants


def test_default_values():
    assert constants.CB_WEBSITE_URL == 'https://www.crunchbase.com'
    assert constants.CB_API_URL == 'https://api.crunchbase.com/api'
    assert constants.CB_API_VERSION == 'v4'
