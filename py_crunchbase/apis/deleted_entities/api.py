import os.path
from typing import List

from ..base import CrunchbaseAPI
from ...paginator import Paginated
from ...query_builder import BaseQueryBuilder
from ...utils import DataDict


class QueryBuilder(BaseQueryBuilder):

    def build(self) -> dict:
        params = super().build()

        if len(self.fields) > 1:
            params['collection_ids'] = ','.join(self.fields)
        if self.order:
            params['deleted_at_order'] = self.order[0][1]

        return params


class DeletedEntitiesAPI(CrunchbaseAPI, Paginated):

    AUTOCOMPLETE_PATH = 'deleted_entities'
    MAX_LIMIT = 2000
    query_builder_cls = QueryBuilder

    def __init__(self, api_key: str = None):
        super().__init__(api_key=api_key)
        self.query_builder = self.query_builder_cls(max_limit=self.MAX_LIMIT)
        self.collection_ids = []

    def _get_path(self):
        if len(self.collection_ids) == 1:
            return os.path.join(self.AUTOCOMPLETE_PATH, self.collection_ids[0])
        return self.AUTOCOMPLETE_PATH

    def select(self, *collection_ids: str):
        if collection_ids:
            collection_ids = list({str(id_) for id_ in collection_ids}.union(self.collection_ids))
            self.collection_ids.extend(collection_ids)
            self.query_builder.add_fields(collection_ids)
        return self

    def limit(self, value: int):
        self.query_builder.add_limit(value)
        return self

    def order_by_deleted_at(self, sort: str = 'asc'):
        self.query_builder.add_order('', sort)
        return self

    def set_next(self, data_list: List[DataDict]):
        self.query_builder.add_next(data_list[-1].uuid)

    def set_previous(self, data_list: List[DataDict]):
        self.query_builder.add_next(data_list[0].uuid)

    def execute(self) -> list:
        return [DataDict(data) for data in self.send_request(self._get_path(), params=self.query_builder.build())]


__all__ = ['DeletedEntitiesAPI']
