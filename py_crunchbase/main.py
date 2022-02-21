from typing import Type

from .apis import SearchAPI, AutoCompleteAPI, EntitiesAPI, DeletedEntitiesAPI
from .entities import Entities, Entity


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
    def _entities_api(self, entity_cls: Type[Entity]) -> EntitiesAPI:
        return EntitiesAPI(entity_cls, api_key=self.api_key)

    def acquisitions_api(self): return self._entities_api(Entities.Acquisition)
    def addresses_api(self): return self._entities_api(Entities.Address)
    def categories_api(self): return self._entities_api(Entities.Category)
    def category_groups_api(self): return self._entities_api(Entities.CategoryGroup)
    def degrees_api(self): return self._entities_api(Entities.Degree)
    def event_appearances_api(self): return self._entities_api(Entities.EventAppearance)
    def events_api(self): return self._entities_api(Entities.Event)
    def funding_rounds_api(self): return self._entities_api(Entities.FundingRound)
    def funds_api(self): return self._entities_api(Entities.Fund)
    def investments_api(self): return self._entities_api(Entities.Investment)
    def ipos_api(self): return self._entities_api(Entities.Ipo)
    def jobs_api(self): return self._entities_api(Entities.Job)
    def locations_api(self): return self._entities_api(Entities.Location)
    def organizations_api(self): return self._entities_api(Entities.Organization)
    def ownerships_api(self): return self._entities_api(Entities.Ownership)
    def people_api(self): return self._entities_api(Entities.Person)
    def press_references_api(self): return self._entities_api(Entities.PressReference)

    # Search APIs
    def _search_api(self, entity_cls: Type[Entity]):
        return SearchAPI(entity_cls, api_key=self.api_key)

    def search_acquisitions_api(self): return self._search_api(Entities.Acquisition)
    def search_addresses_api(self): return self._search_api(Entities.Address)
    def search_categories_api(self): return self._search_api(Entities.Category)
    def search_category_groups_api(self): return self._search_api(Entities.CategoryGroup)
    def search_degrees_api(self): return self._search_api(Entities.Degree)
    def search_event_appearances_api(self): return self._search_api(Entities.EventAppearance)
    def search_events_api(self): return self._search_api(Entities.Event)
    def search_funding_rounds_api(self): return self._search_api(Entities.FundingRound)
    def search_funds_api(self): return self._search_api(Entities.Fund)
    def search_investments_api(self): return self._search_api(Entities.Investment)
    def search_ipos_api(self): return self._search_api(Entities.Ipo)
    def search_jobs_api(self): return self._search_api(Entities.Job)
    def search_key_employee_changes_api(self): return self._search_api(Entities.KeyEmployeeChange)
    def search_layoffs_api(self): return self._search_api(Entities.Layoff)
    def search_locations_api(self): return self._search_api(Entities.Location)
    def search_organizations_api(self): return self._search_api(Entities.Organization)
    def search_ownerships_api(self): return self._search_api(Entities.Ownership)
    def search_people_api(self): return self._search_api(Entities.Person)
    def search_press_references_api(self): return self._search_api(Entities.PressReference)
    def search_principals_api(self): return self._search_api(Entities.Principal)
