from typing import Type, List

from .base import CrunchbaseAPI
from ..entities import Entity
from ..paginator import Paginated
from ..query_builder import QueryBuilder


class SearchAPI(CrunchbaseAPI, Paginated):

    query_builder_cls = QueryBuilder
    DEFAULT_FIELDS = query_builder_cls.DEFAULT_FIELDS

    def __init__(self, entity: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.path = f'searches/{entity.API_PATH}'
        self.query_builder = self.query_builder_cls(entity)
        self.entity = entity

    def reset(self):
        """
        clears the query builder
        """
        self.query_builder = self.query_builder_cls(self.entity)

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

    def set_next(self, entities: List[Type[Entity]]):
        if entities:
            self.query_builder.add_next(entities[-1].uuid)

    def set_previous(self, entities: List[Type[Entity]]):
        if entities:
            self.query_builder.add_previous(entities[0].uuid)

    def execute(self) -> list:
        """
        returns list of entities returned by request
        """
        data = self.send_request(self.path, method_name='post', payload=self.query_builder.build())
        return [self.entity(entity) for entity in data['entities']]


__all__ = ['SearchAPI']
