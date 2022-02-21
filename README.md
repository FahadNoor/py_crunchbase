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

# If both are provided, the latter will take preference
```

### Autocomplete API
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()

api = pycb.autocomplete_api()

# search 'crunchbase' across all entities
for entity in api.autocomplete('crunchbase').execute():
    print(entity.permalink, entity.uuid)
```

### Deleted Entities API
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()

api = pycb.deleted_entities_api()

# Paginate through deleted entities
for page in api.iterate():
    for entity in page:
        print(entity.uuid, entity.deleted_at)
```

### Entities API
PyCrunchbase provides a method per entity type for entities API. For example:
- organizations_api = pycb.organizations_api()
- people_api = pycb.people_api()

You can check complete list in PyCrunchbase class.
#### Entities API for Organizations
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()

org_api = pycb.organizations_api()

# pass entity_def_id of the organization. For example 'crunchbase' is entity_def_id of Crunchbase organization
entities_api = org_api.get_entities_api('crunchbase')

# following will get information of Crunchbase organization with all of it's fields
entity = entities_api.select_all().execute()
print(entity.uuid, entity.entity_def_id)
```
#### Entities Card API for Organizations
```python
from py_crunchbase import PyCrunchbase, Cards

pycb = PyCrunchbase()

org_api = pycb.organizations_api()

cards_api = org_api.get_cards_api('crunchbase', Cards.Organization.press_references)

# get_entities_api and get_card_apis methods accept entity instance too
# org_cards_api = org_api.get_cards_api(entity, Cards.Organization.press_references)

# Paginate through entity's cards
for entity in cards_api.iterate():
    for card_name, values in entity.cards.items():
        for card in values:
            print(card.uuid, card.entity_def_id)
```

### Search API
Search API also has a method per entity type. For example:
- search_org_api = pycb.search_organizations_api()
- search_people_api = pycb.search_people_api()

You can check complete list in PyCrunchbase class.
Below is an exaple of Search API for Organizations
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()

api = pycb.search_organizations_api()

# get contact email of organizations whose founder's permalink is michael-arrington
# order results by founded on date, limit results to 5
api.select('contact_email').where(
    founder_identifiers__includes=['michael-arrington']
).order_by('founded_on', 'desc').limit(5)

# iterate through entities
for page in api.iterate():
    for entity in page:
        print(entity.uuid, entity.permalink)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)