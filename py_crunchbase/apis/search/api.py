from typing import Type, List

from .query_builder import SearchQueryBuilder
from ..base import CrunchbaseAPI
from ...entities import Entity
from ...paginator import Paginated


class SearchAPI(CrunchbaseAPI, Paginated):

    query_builder_cls = SearchQueryBuilder

    def __init__(self, entity_cls: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.path = f'searches/{entity_cls.api_path()}'
        self.query_builder = self.query_builder_cls(entity_cls)
        self.entity_cls = entity_cls

    def reset(self):
        """
        clears the query builder
        """
        self.query_builder = self.query_builder_cls(self.entity_cls)

    def select(self, *names) -> 'SearchAPI':
        self.query_builder.add_fields(names)
        return self

    def where(self, **kwargs) -> 'SearchAPI':
        for field__operator, value in kwargs.items():
            self.query_builder.add_query(field__operator, value)
        return self

    def order_by(self, field: str, sort: str = 'asc') -> 'SearchAPI':
        self.query_builder.add_order(field, sort)
        return self

    def limit(self, value: int) -> 'SearchAPI':
        self.query_builder.add_limit(value)
        return self

    def set_next(self, entities: List[Entity]):
        if entities:
            self.query_builder.add_next(entities[-1].uuid)

    def set_previous(self, entities: List[Entity]):
        if entities:
            self.query_builder.add_previous(entities[0].uuid)

    def execute(self) -> list:
        """
        returns list of entities returned by request
        """
        data = self.send_request(self.path, method_name='post', payload=self.query_builder.build())
        return [self.entity_cls(entity['properties']) for entity in data['entities']]


__all__ = ['SearchAPI']
