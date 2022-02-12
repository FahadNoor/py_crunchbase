from typing import Type, List

from .base import CrunchbaseAPI
from ..entities import Entity
from ..query_builder import QueryBuilder


class SearchAPI(CrunchbaseAPI):

    query_builder_cls = QueryBuilder
    DEFAULT_FIELDS = query_builder_cls.DEFAULT_FIELDS

    def __init__(self, resource: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.path = f'searches/{resource.API_PATH}'
        self.query_builder = self.query_builder_cls(resource)
        self.resource = resource

    def reset(self):
        """
        clears the query builder
        """
        self.query_builder = self.query_builder_cls(self.resource)

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

    def add_next(self, resources: List[Type[Entity]]):
        if resources:
            self.query_builder.add_next(resources[-1].uuid)

    def add_previous(self, resources: List[Type[Entity]]):
        if resources:
            self.query_builder.add_previous(resources[0].uuid)

    def execute_search(self) -> list:
        """
        returns list of entities returned by request
        """
        data = self.send_request(self.path, method_name='post', payload=self.query_builder.build())
        return [self.resource(entity) for entity in data['entities']]

    def search(self) -> 'Paginator':
        """
        returns Paginator to go through pages
        Usage:
        for page in search_api.search():
            for resource in page:
                print(resource.uuid)
        """
        return Paginator(self)


class Paginator:

    def __init__(self, api: SearchAPI):
        self.api = api
        self.current_list = None

    def next(self):
        if self.current_list is not None:
            self.api.add_next(self.current_list)

        self.current_list = self.api.execute_search()
        return self.current_list

    def previous(self):
        if self.current_list is not None:
            self.api.add_previous(self.current_list)

        self.current_list = self.api.execute_search()
        return self.current_list

    def __iter__(self):
        return self

    def __next__(self):
        data = self.next()
        if not data:
            raise StopIteration
        return data


__all__ = ['SearchAPI']
