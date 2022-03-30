import os

CB_WEBSITE_URL = os.getenv('PY_CRUNCHBASE_WEBSITE_URL', 'https://www.crunchbase.com')
CB_API_URL = os.getenv('PY_CRUNCHBASE_API_URL', 'https://api.crunchbase.com/api')
CB_API_VERSION = os.getenv('PY_CRUNCHBASE_API_VERSION', 'v4')
