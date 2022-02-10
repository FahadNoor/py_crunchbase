from .resources import CBR
from .search import SearchAPI
from .autocomplete import AutoCompleteAPI
from .entities import EntitiesAPI


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
        companies = search_api.execute_search()
    except search_api.Exception as exc:
        raise

    # or through pagination
    try:
        for page in search_api.search():
            for company in page:
                print(company.uuid)
    except search_api.Exception as exc:
        raise

    ####################
    Example # 2: Search People

    search_api = pycb.search_people()
    search_api.select('name', 'facebook', 'linkedin', 'twitter').where(uuid__includes=uuids).limit(100)
    try:
        people = search_api.execute_search()
    except search_api.Exception as exc:
        raise


    ####################
    Example # 3: Autocomplete

    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    # SEARCH APIs

    def search_organizations(self) -> SearchAPI:
        return SearchAPI(CBR.Organization, api_key=self.api_key)

    def search_people(self) -> SearchAPI:
        return SearchAPI(CBR.Person, api_key=self.api_key)

    # AUTOCOMPLETE API

    def autocomplete(self, query: str, *collection_ids) -> AutoCompleteAPI:
        return AutoCompleteAPI(query, *collection_ids, api_key=self.api_key)

    # ENTITIES APIs

    def organizations(self) -> EntitiesAPI:
        return EntitiesAPI(CBR.Organization, api_key=self.api_key)

    def people(self) -> EntitiesAPI:
        return EntitiesAPI(CBR.Person, api_key=self.api_key)
