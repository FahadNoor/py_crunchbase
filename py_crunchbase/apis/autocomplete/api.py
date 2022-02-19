from ..base import CrunchbaseAPI
from ...utils import DataDict


class AutoCompleteAPI(CrunchbaseAPI):

    AUTOCOMPLETE_PATH = 'autocompletes'
    MAX_LIMIT = 25

    def __init__(self, query: str, *collection_ids, api_key: str = None):
        super().__init__(api_key=api_key)
        self.query = query
        self.collection_ids = [str(id_) for id_ in collection_ids]

    def execute(self, limit: int = None):
        params = {'query': self.query}

        if self.collection_ids:
            params['collection_ids'] = ','.join(self.collection_ids)

        if limit:
            params['limit'] = min(limit, self.MAX_LIMIT)

        data = self.send_request(self.AUTOCOMPLETE_PATH, params=params)
        return [DataDict(entity) for entity in data['entities']]


__all__ = ['AutoCompleteAPI']
