# PyCrunchbase

PyCrunchbase is a python client for Crunchbase's [REST API](https://app.swaggerhub.com/apis-docs/Crunchbase/crunchbase-enterprise_api/1.0.3#/).
Crunchbase provides 4 types of APIs:-

1. [Search API](#search-api)
2. [Autocomplete API](#autocomplete-api)
3. [Deleted Entities API](#deleted-entities-api)
4. [Entities API](#entities-api)

PyCrunchbase supports all of these through a very simple interface.

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

#### [Find funding rounds since 2012 that have 4+ investors & raised $10M+ USD](https://data.crunchbase.com/docs/examples-search-api#example-1-find-funding-rounds-since-2012-that-have-4-investors--raised-10m-usd)
```python
from py_crunchbase import PyCrunchbase
from py_crunchbase.apis.search.predicates import Currency

pycb = PyCrunchbase()
api = pycb.search_funding_rounds_api()

api.select(
    'identifier', 'announced_on', 'funded_organization_identifier', 'money_raised', 'investment_type'
).where(
    announced_on__gte=2012, num_investors__lte=4, money_raised__gte=Currency(10000000)
).order_by(
    'announced_on'
)

for page in api.iterate():
    for funding_round in page:
        print(funding_round.permalink)
```

#### [Find companies in Europe w/ $25M-$100M USD in funding](https://data.crunchbase.com/docs/examples-search-api#example-2-find-companies-in-europe-w-25m-100m-usd-in-funding)
```python
from py_crunchbase import PyCrunchbase, Entities
from py_crunchbase.apis.search.predicates import Currency

pycb = PyCrunchbase()
api = pycb.search_organizations_api()

org_facet_ids = Entities.Organization.Facets
api.select(
    'identifier', 'categories', 'location_identifiers', 'short_description', 'rank_org'
).where(
    funding_total__between=[Currency(25000000), Currency(100000000)],
    location_identifiers__includes=['6106f5dc-823e-5da8-40d7-51612c0b2c4e'],
    facet_ids__includes=[org_facet_ids.company]
).order_by(
    'rank_org'
)

for page in api.iterate():
    for company in page:
        print(company.permalink)
```

#### [Find Biotech companies w/ 101-250 number of employees](https://data.crunchbase.com/docs/examples-search-api#example-3-find-biotech-companies-w-101-250-number-of-employees)
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
)

for page in api.iterate():
    for company in page:
        print(company.permalink)
```

### Autocomplete API

#### [Find any entities that best matches "box"](https://data.crunchbase.com/docs/examples-autocomplete-api#example-1-use-autocomplete-to-find-any-entities-that-best-matches-box)
```python
from py_crunchbase import PyCrunchbase

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

for entity in api.autocomplete('box').limit(15).execute():
    print(entity.permalink, entity.uuid)
```

#### [Find an investor that best matches "mayfield"](https://data.crunchbase.com/docs/examples-autocomplete-api#example-2-use-autocomplete-to-find-an-investor-that-best-matches-mayfield)
```python
from py_crunchbase import PyCrunchbase, Collections

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

for entity in api.autocomplete('mayfield').select_collections(Collections.Principals.investors).execute():
    print(entity.permalink, entity.uuid)
```

#### [Find a category or category group that best matches "mobile payment"](https://data.crunchbase.com/docs/examples-autocomplete-api#example-3-use-autocomplete-to-find-a-category-or-category-group-that-best-matches-mobile-payment)
```python
from py_crunchbase import PyCrunchbase, Collections

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

for entity in api.autocomplete('mobile payment').select_collections(
        Collections.Categories, Collections.CategoryGroups
).limit(10).execute():
    print(entity.permalink, entity.uuid)
```

#### [Find a company that best matches "airbnb"](https://data.crunchbase.com/docs/examples-autocomplete-api#example-3-use-autocomplete-to-find-a-category-or-category-group-that-best-matches-mobile-payment)
```python
from py_crunchbase import PyCrunchbase, Collections

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

for entity in api.autocomplete('airbnb').select_collections(Collections.Organizations.companies).execute():
    print(entity.permalink, entity.uuid)
```

#### [Find a country or city that best matches "united"](https://data.crunchbase.com/docs/examples-autocomplete-api#example-5-use-autocomplete-to-find-a-country-or-city-that-best-matches-united)
```python
from py_crunchbase import PyCrunchbase, Collections

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

for entity in api.autocomplete('united').select_collections(
        Collections.Locations.countries, Collections.Locations.cities
).limit(10).execute():
    print(entity.permalink, entity.uuid)
```

### Deleted Entities API
```python
from py_crunchbase import PyCrunchbase, Collections

pycb = PyCrunchbase()

api = pycb.deleted_entities_api()

for page in api.select_collections(
        Collections.Organizations, Collections.People, Collections.FundingRounds, Collections.Events
).order_by_deleted_at().iterate():
    for entity in page:
        print(entity.uuid, entity.deleted_at)
```

### Entities API
#### [Retrieve information for Tesla Motors](https://data.crunchbase.com/docs/examples-entity-lookup-api#example-1-retrieve-information-for-tesla-motors)
```python
from py_crunchbase import PyCrunchbase, Cards

pycb = PyCrunchbase()

org_api = pycb.organizations_api()

cards = Cards.Organization
entity = org_api.get(
    entity_id='tesla-motors',
    field_ids=['website', 'facebook', 'categories', 'short_description', 'founded_on', 'rank_org_company'],
    card_ids=[cards.founders, cards.raised_funding_rounds]
)

print(entity.website, entity.cards)
```
#### [Get more results for Sequoia Capital's investments](https://data.crunchbase.com/docs/examples-entity-lookup-api#example-2-paginate-get-more-results-for-sequoia-capitals-investments)

```python
from py_crunchbase import PyCrunchbase, Cards

pycb = PyCrunchbase()

org_api = pycb.organizations_api()

cards = Cards.Organization
card_list = org_api.get_cards(
    entity_id='sequoia-capital',
    card_id=cards.participated_investments,
    card_field_ids=['announced_on', 'funding_round_money_raised', 'organization_identifier', 'partner_identifiers'],
    order_by=('funding_round_money_raised', 'desc')
)

for card in card_list:
    print(card.uuid)

```
## Extras

### Entities
Each Crunchbase Entity has its own class and can be accessed through `Entities`
```python
from py_crunchbase import Entities

Organization = Entities.Organization
Person = Entities.Person
```
Entity classes can be extended through a decorator
```python
from py_crunchbase import Entities
from py_crunchbase.decorators import override_entity

@override_entity(Entities.Organization)
class CustomOrganization(Entities.Organization):
    pass

# now Entities.Organization will return CustomOrganization
```
### Cards
Each Entity class defines its own cards (if any) and can be accessed through `Cards`
```python
from py_crunchbase import Cards

OrgCards = Cards.Organization
print(OrgCards.investors)
print(OrgCards.founders)

# all available Org cards
print(OrgCards.all())
```
### Collections
Collections are also defined in Entity class and can be accessed through `Collections`
```python
from py_crunchbase import Collections

OrgCol = Collections.Organizations
print(OrgCol.companies)
print(OrgCol.schools)
```

### Exception Handling
There are two ways to catch exceptions
```python
from py_crunchbase import PyCrunchbase, CrunchbaseAPIException

pycb = PyCrunchbase()
api = pycb.autocomplete_api()

try:
    entities = api.autocomplete('box').limit(15).execute()
except api.Exception:
    pass

# OR through CrunchbaseAPIException

try:
    entities = api.autocomplete('box').limit(15).execute()
except CrunchbaseAPIException:
    pass
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)