from typing import Union, Type

from .base import BaseEntitiesAPI
from ...entities import Entity, CardType
from ...utils import is_iterable


class EntitiesAPI(BaseEntitiesAPI):

    ALL_FIELDS = '__ALL__'

    def __init__(self, entity_id: Union[str, Entity], entity_cls: Type[Entity], api_key: str = None):
        super().__init__(entity_cls=entity_cls, api_key=api_key)
        self.entity_id = self._get_entity_id(entity_id)
        self.field_ids = []
        self.card_ids = []

    def select(self, *field_ids: str) -> 'EntitiesAPI':
        if field_ids:
            if field_ids[0] == self.ALL_FIELDS:
                if CardType.fields not in self.card_ids:
                    self.card_ids.append(CardType.fields)
            else:
                self.field_ids = list(set(field_ids).union(self.field_ids))
        return self

    def select_all(self) -> 'EntitiesAPI':
        self.select(self.ALL_FIELDS)
        return self

    def select_cards(self, card_ids: Union[list, str]) -> 'EntitiesAPI':
        if card_ids:
            card_ids = set(card_ids) if is_iterable(card_ids) else {card_ids}
            self.card_ids = list(card_ids.union(self.card_ids))
        return self

    def execute(self) -> Entity:
        params = {}

        if self.field_ids:
            params['field_ids'] = ','.join(self.field_ids)

        if self.card_ids:
            params['card_ids'] = ','.join(self.card_ids)

        path = self._get_path(self.entity_id)
        data = self.send_request(path, params=params or None)
        return self._parse_response_data(data)


__all__ = ['EntitiesAPI']
