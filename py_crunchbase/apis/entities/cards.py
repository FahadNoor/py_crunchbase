from typing import Union, Type, List

from .base import BaseEntitiesAPI
from ...entities import Entity
from ...paginator import Paginated, Paginator
from ...query_builder import BaseQueryBuilder


class CardsAPIPaginator(Paginator):

    def __next__(self):
        entity = self.next()
        if not entity or not entity.cards:
            raise StopIteration
        return entity


class CardsAPIQueryBuilder(BaseQueryBuilder):

    def validate_fields(self, names):
        pass

    def build(self) -> dict:
        params = {}

        if self.fields:
            self.fields = list(set(self.fields))
            params['card_field_ids'] = ','.join(self.fields)
        if self.next_id:
            params['after_id'] = self.next_id
        if self.previous_id:
            params['before_id'] = self.previous_id
        if self.order:
            params['order'] = ','.join(self.order[0])
        if self.limit:
            params['limit'] = self.limit

        return params


class CardsAPI(BaseEntitiesAPI, Paginated):

    query_builder_cls = CardsAPIQueryBuilder
    paginator_cls = CardsAPIPaginator

    def __init__(self, entity_id: Union[str, Entity], card_id: str, entity_cls: Type[Entity], api_key: str = None):
        super().__init__(entity_cls=entity_cls, api_key=api_key)
        self.query_builder = self.query_builder_cls()
        self.entity_id = self._get_entity_id(entity_id)
        self.card_id = card_id

    def select(self, *field_ids: str):
        if field_ids:
            self.query_builder.add_fields(field_ids)
        return self

    def order_by(self, field: str, sort: str = 'asc'):
        self.query_builder.add_order(field, sort)
        return self

    def limit(self, value: int):
        self.query_builder.add_limit(value)
        return self

    def set_next(self, entity: Entity):
        if entity.cards:
            try:
                card_list = list(entity.cards.values())[0]
                self.query_builder.add_next(card_list[-1].uuid)
            except KeyError:
                pass

    def set_previous(self, entity: Entity):
        if entity.cards:
            try:
                card_list = list(entity.cards.values())[0]
                self.query_builder.add_previous(card_list[0].uuid)
            except KeyError:
                pass

    def execute(self):
        path = self._get_path(self.entity_id, self.card_id)
        return self._parse_response_data(self.send_request(path, params=self.query_builder.build()))

