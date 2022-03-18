from typing import Union, Type

from .base_ import BaseEntitiesAPI
from ...entities import Entity
from ...paginator import Paginated, Paginator as BasePaginator
from ...query_builder import BaseQueryBuilder


class Paginator(BasePaginator):

    def __next__(self) -> Entity:
        entity = self.next()
        if not entity or not entity.cards:
            raise StopIteration
        return entity


class QueryBuilder(BaseQueryBuilder):

    def build(self) -> dict:
        params = super().build()

        if self.order:
            params['order'] = ','.join(self.order[0])
        if self.fields:
            params['card_field_ids'] = ','.join(self.fields)

        return params


class CardsAPI(BaseEntitiesAPI, Paginated):

    query_builder_cls = QueryBuilder
    paginator_cls = Paginator
    MAX_LIMIT = 100

    def __init__(self, entity_id: Union[str, Entity], card_id: str, entity_cls: Type[Entity], api_key: str = None):
        super().__init__(entity_cls=entity_cls, api_key=api_key)
        self.query_builder = self.query_builder_cls(max_limit=self.MAX_LIMIT)
        self.entity_id = self._get_entity_id(entity_id)
        self.card_id = card_id

    def select(self, *field_ids: str) -> 'CardsAPI':
        if field_ids:
            self.query_builder.add_fields(field_ids)
        return self

    def order_by(self, field: str, sort: str = 'asc') -> 'CardsAPI':
        self.query_builder.add_order(field, sort)
        return self

    def limit(self, value: int) -> 'CardsAPI':
        self.query_builder.add_limit(value)
        return self

    def set_next(self, entity: Entity):
        cards = entity.cards or {}
        card_list = list(cards.values())[0]
        self.query_builder.add_next(card_list[-1].uuid)

    def set_previous(self, entity: Entity):
        cards = entity.cards or {}
        card_list = list(cards.values())[0]
        self.query_builder.add_previous(card_list[0].uuid)

    def execute(self) -> Entity:
        path = self._get_path(self.entity_id, self.card_id)
        return self._parse_response_data(self.send_request(path, params=self.query_builder.build()))
