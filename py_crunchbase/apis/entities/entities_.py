from typing import Union, Type

from .base_ import BaseEntitiesAPI
from ...entities import Entity, BaseCards


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
                if BaseCards.fields not in self.card_ids:
                    self.card_ids.append(BaseCards.fields)
            else:
                self.field_ids = list(set(field_ids).union(self.field_ids))
        return self

    def select_all(self) -> 'EntitiesAPI':
        return self.select(self.ALL_FIELDS)

    def select_cards(self, *card_ids: str) -> 'EntitiesAPI':
        if card_ids:
            self.card_ids = list(set(card_ids).union(self.card_ids))
        return self

    def select_all_cards(self) -> 'EntitiesAPI':
        if self.entity_cls.Cards:
            self.select_cards(*self.entity_cls.Cards.all())
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
