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
from py_crunchbase import PyCrunchbase

# API key can be set as the env variable PY_CRUNCHBASE_API_KEY 
pycb = PyCrunchbase()

# OR passed as an argument
pycb = PyCrunchbase('api_key')

# If both are provided, API key passed as an argument will take preference
```

### Autocomplete API
```python
from py_crunchbase import PyCrunchbase, Collections
pycb = PyCrunchbase()

# search 'crunchbase' across all entities
api = pycb.autocomplete_api()
try:
    entities = api.search('crunchbase').execute()
except api.Exception as exc:
    print(exc)
    raise

for entity in entities:
    print(entity.permalink)

# Providing Additional arguments
api = pycb.autocomplete_api()

# provide query
api.search('crunchbase')

# limit results to 5 entities
api.limit(5)

# search across organizations and funds
api.select_collections(Collections.Organizations, Collections.Funds)

# Collections provide facet names to narrow down the search
api.select_collections(Collections.Organizations.companies, Collections.Funds)

# select_collections can be called multiple times
api.select_collections(Collections.Organizations.investors).select_collections(Collections.Events)

# now calling execute will apply the provided arguments
entities = api.execute()

# api methods are chainable
entities = api.search('crunchbase').limit(5).select_collections(Collections.Organizations).execute()
```

### Deleted Entities API
```python
from py_crunchbase import PyCrunchbase, Collections
pycb = PyCrunchbase()

# Get deleted entities
api = pycb.deleted_entities_api()
try:
    entities = api.execute()    # by default, it will return 100 entities
except api.Exception:
    raise

for entity in entities:
    print(entity.uuid, entity.deleted_at)

# Providing Additional arguments
api = pycb.deleted_entities_api()

# filter by collection ids
api.select_collections(Collections.People, Collections.Events)

# limit 50 entities per page
api.limit(50)

# order by deleted at asc/desc
api.order_by_deleted_at(sort='desc')

# get first 50 entities
entities = api.execute()

# update api to get next page
api.set_next(entities)

# now execute will return next 50 entities
entities = api.execute()

# update api to get previous page
api.set_previous(entities)

# now execute will return previous 50 entities
entities = api.execute()

# API also provides an iterator to go through pages easily
for page in api.limit(50).order_by_deleted_at().iterate():
    for entity in page:
        print(entity.uuid)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)