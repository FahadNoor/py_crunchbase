from typing import List

from ..base import CrunchbaseAPI
from ...utils import DataDict


class AutoCompleteAPI(CrunchbaseAPI):

    AUTOCOMPLETE_PATH = 'autocompletes'
    MAX_LIMIT = 25

    def __init__(self, api_key: str = None):
        super().__init__(api_key=api_key)
        self.query = None
        self.collection_ids = []
        self.limit_value = None

    def search(self, query: str) -> 'AutoCompleteAPI':
        self.query = query
        return self

    def select_collections(self, *collection_ids: str) -> 'AutoCompleteAPI':
        if collection_ids:
            self.collection_ids = list({str(id_) for id_ in collection_ids}.union(self.collection_ids))
        return self

    def limit(self, value: int) -> 'AutoCompleteAPI':
        self.limit_value = value
        return self

    def execute(self) -> List[DataDict]:
        if not self.query:
            raise ValueError(f'{self.query} is not a valid query')

        params = {'query': self.query}

        if self.collection_ids:
            params['collection_ids'] = ','.join(self.collection_ids)

        if self.limit_value:
            params['limit'] = min(self.limit_value, self.MAX_LIMIT)

        data = self.send_request(self.AUTOCOMPLETE_PATH, params=params)
        return [DataDict(entity) for entity in data['entities']]


__all__ = ['AutoCompleteAPI']
