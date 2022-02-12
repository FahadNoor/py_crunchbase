from .apis import SearchAPI, AutoCompleteAPI, EntitiesAPI
from .entities import ER


class PyCrunchbase:
    """
    This is the main interface of PyCrunchbase API.
    Api key can be passed while creating its instance or set as env variable PY_CRUNCHBASE_API_KEY

    pycb = PyCrunchbase('api_key')

    ####################
    Example # 1: Search Organizations

    search_api = pycb.search_organizations()
    search_api.select('contact_email', 'founder_identifiers').where(website_url__domain_eq='www.abc.com').limit(100)

    # get all companies at once
    try:
        companies = search_api.execute()
    except search_api.Exception as exc:
        raise

    # or through pagination
    try:
        for page in search_api.iterate():
            for company in page:
                print(company.uuid)
    except search_api.Exception as exc:
        raise

    ####################
    Example # 2: Search People

    search_api = pycb.search_people()
    search_api.select('name', 'facebook', 'linkedin', 'twitter').where(uuid__includes=uuids).limit(100)
    try:
        people = search_api.execute()
    except search_api.Exception as exc:
        raise


    ####################
    Example # 3: Autocomplete

    """
    SEARCH_API_METHOD_PREFIX = 'search_'
    ENTITIES_API_METHOD_SUFFIX = '_api'

    # The keys of this dict with SEARCH_API_METHOD_PREFIX represent search APIs. i.e.
    # search_organizations() or search_people()
    SEARCH_APIS = {entity.API_PATH: entity for entity in ER.all()}

    # The keys of this dict with ENTITIES_API_METHOD_SUFFIX represent entities APIs. i.e.
    # organizations_api() or people_api()
    ENTITY_APIS = {
        entity.API_PATH: entity for entity in ER.all()
        if entity not in (ER.KeyEmployeeChange, ER.Layoff, ER.Principal)
    }

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def __getattr__(self, name: str):

        # check if it's a search api method
        if name.startswith(self.SEARCH_API_METHOD_PREFIX):
            api_name = name[len(self.SEARCH_API_METHOD_PREFIX):]
            if api_name in self.SEARCH_APIS:
                return lambda: SearchAPI(self.SEARCH_APIS[api_name], api_key=self.api_key)

        # check if it's an entities api method
        if name.endswith(self.ENTITIES_API_METHOD_SUFFIX):
            api_name = name[:len(self.ENTITIES_API_METHOD_SUFFIX)]
            if api_name in self.ENTITY_APIS:
                return lambda: EntitiesAPI(self.ENTITY_APIS[api_name], api_key=self.api_key)

        raise AttributeError

    def autocomplete(self, query: str, *collection_ids) -> AutoCompleteAPI:
        return AutoCompleteAPI(query, *collection_ids, api_key=self.api_key)
