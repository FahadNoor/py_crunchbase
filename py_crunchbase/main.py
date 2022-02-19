from typing import Type

from .apis import SearchAPI, AutoCompleteAPI, EntitiesAPI, DeletedEntitiesAPI
from .entities import ER, Entity


class PyCrunchbase:
    """
    This is the main interface of PyCrunchbase API.
    Api key can be passed while creating its instance or set as env variable (PY_CRUNCHBASE_API_KEY)
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    # Autocomplete API
    def autocomplete_api(self) -> AutoCompleteAPI:
        return AutoCompleteAPI(api_key=self.api_key)

    # Deleted Entities API
    def deleted_entities_api(self) -> DeletedEntitiesAPI:
        return DeletedEntitiesAPI(api_key=self.api_key)

    # Entities APIs
    def _entities_api(self, entity_cls: Type[Entity]):
        return EntitiesAPI(entity_cls, api_key=self.api_key)

    def acquisitions_api(self): return self._entities_api(ER.Acquisition)
    def addresses_api(self): return self._entities_api(ER.Address)
    def categories_api(self): return self._entities_api(ER.Category)
    def category_groups_api(self): return self._entities_api(ER.CategoryGroup)
    def degrees_api(self): return self._entities_api(ER.Degree)
    def event_appearances_api(self): return self._entities_api(ER.EventAppearance)
    def events_api(self): return self._entities_api(ER.Event)
    def funding_rounds_api(self): return self._entities_api(ER.FundingRound)
    def funds_api(self): return self._entities_api(ER.Fund)
    def investments_api(self): return self._entities_api(ER.Investment)
    def ipos_api(self): return self._entities_api(ER.Ipo)
    def jobs_api(self): return self._entities_api(ER.Job)
    def locations_api(self): return self._entities_api(ER.Location)
    def organizations_api(self): return self._entities_api(ER.Organization)
    def ownerships_api(self): return self._entities_api(ER.Ownership)
    def people_api(self): return self._entities_api(ER.Person)
    def press_references_api(self): return self._entities_api(ER.PressReference)

    # Search APIs
    def _search_api(self, entity_cls: Type[Entity]):
        return SearchAPI(entity_cls, api_key=self.api_key)

    def search_acquisitions_api(self): return self._search_api(ER.Acquisition)
    def search_addresses_api(self): return self._search_api(ER.Address)
    def search_categories_api(self): return self._search_api(ER.Category)
    def search_category_groups_api(self): return self._search_api(ER.CategoryGroup)
    def search_degrees_api(self): return self._search_api(ER.Degree)
    def search_event_appearances_api(self): return self._search_api(ER.EventAppearance)
    def search_events_api(self): return self._search_api(ER.Event)
    def search_funding_rounds_api(self): return self._search_api(ER.FundingRound)
    def search_funds_api(self): return self._search_api(ER.Fund)
    def search_investments_api(self): return self._search_api(ER.Investment)
    def search_ipos_api(self): return self._search_api(ER.Ipo)
    def search_jobs_api(self): return self._search_api(ER.Job)
    def search_key_employee_changes_api(self): return self._search_api(ER.KeyEmployeeChange)
    def search_layoffs_api(self): return self._search_api(ER.Layoff)
    def search_locations_api(self): return self._search_api(ER.Location)
    def search_organizations_api(self): return self._search_api(ER.Organization)
    def search_ownerships_api(self): return self._search_api(ER.Ownership)
    def search_people_api(self): return self._search_api(ER.Person)
    def search_press_references_api(self): return self._search_api(ER.PressReference)
    def search_principals_api(self): return self._search_api(ER.Principal)
