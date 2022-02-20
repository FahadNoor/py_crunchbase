# PyCrunchbase

PyCrunchbase is a python client for Crunchbase's [REST API](https://app.swaggerhub.com/apis-docs/Crunchbase/crunchbase-enterprise_api/1.0.3#/) (v4).
Crunchbase provides 4 types of APIs:-

1. Autocomplete API
2. Deleted Entities API
3. Entities API
4. Search API

PyCrunchbase supports all 4 APIs through a very simple interface.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyCrunchbase.

```bash
pip install py_crunchbase
```

## Usage

```python
from py_crunchbase import PyCrunchbase, Collections

# API key can be set as the env variable PY_CRUNCHBASE_API_KEY or passed as an argument. 
pycb = PyCrunchbase()  # or pycb = PyCrunchbase('api_key')

#### Autocomplete API ####
api = pycb.autocomplete_api()
try:
    data_list = api.search('crunchbase').execute()
except api.Exception as exc:
    print(exc)

# To provide collection ids or limit
try:
    data_list = api.search('crunchbase').select_collections(
        Collections.Organization, Collections.Person
    ).limit(5).execute()
    for data in data_list:
        print(data.uuid)
except api.Exception:
    pass



```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)