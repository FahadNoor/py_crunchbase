# PyCrunchbase

PyCrunchbase is a python client for Crunchbase's [REST API](https://app.swaggerhub.com/apis-docs/Crunchbase/crunchbase-enterprise_api/1.0.3#/) (v4).
Crunchbase provides 4 types of APIs:-

1. Search API
2. Autocomplete API
3. Deleted Entities API
4. Entities API

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

### Search API

#### Companies in Europe with funding total between 25m and 100m USD
```python
from py_crunchbase import PyCrunchbase, Collections
from py_crunchbase.apis.search.predicates import Currency

pycb = PyCrunchbase()

api = pycb.search_organizations_api()

api.select(
    'identifier', 'categories', 'location_identifiers', 'short_description', 'rank_org'
).where(
    funding_total__between=[Currency(25000000), Currency(100000000)],
    location_identifiers__includes=['6106f5dc-823e-5da8-40d7-51612c0b2c4e'],
    facet_ids__includes=[Collections.Organizations.companies]
).order_by(
    'rank_org'
).limit(50)

# iterate through companies
for page in api.iterate():
    for company in page:
        print(company.permalink)
```

#### Biotech companies with number of employees between 101 and 250
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()

api = pycb.search_organizations_api()

api.select(
    'identifier', 'categories', 'location_identifiers', 'short_description', 'rank_org'
).where(
    num_employees_enum__includes=['c_00101_00250'],
    categories__includes=['58842728-7ab9-5bd1-bb67-e8e55f6520a0']
).order_by(
    'rank_org'
).limit(50)

# iterate through companies
for page in api.iterate():
    for company in page:
        print(company.permalink)
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
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)