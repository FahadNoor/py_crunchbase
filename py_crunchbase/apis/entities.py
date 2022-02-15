import os.path
from typing import Union, Type

from .base import CrunchbaseAPI
from ..entities import Entity
from ..utils import is_iterable


class EntitiesAPI(CrunchbaseAPI):

    ENTITIES_PATH = 'entities'
    CARDS_PATH = 'cards'

    def __init__(self, entity: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.entity = entity

    def _get_entity_id(self, entity) -> str:
        if not isinstance(entity, Entity):
            return entity
        if not isinstance(entity, self.entity):
            raise self.Exception(f'Entity should be an instance of {self.entity.__name__}')
        return entity.uuid or entity.identifier.permalink or ''

    def _get_path(self, entity_id: str, card_id: str = None):
        path = os.path.join(self.ENTITIES_PATH, self.entity.API_PATH, entity_id)
        if card_id:
            path = os.path.join(path, self.CARDS_PATH, card_id)
        return path

    def get(self, entity_id: Union[str, Entity], *field_ids: str, card_ids: Union[list, str] = None) -> Entity:

        entity_id = self._get_entity_id(entity_id)
        if card_ids:
            card_ids = list(card_ids) if is_iterable(card_ids) else [card_ids]
        else:
            card_ids = []
        params = {}
        if field_ids and 'fields' not in card_ids:
            params['field_ids'] = ','.join(field_ids)
        if card_ids:
            params['card_ids'] = ','.join(card_ids)

        path = self._get_path(entity_id)
        return self.entity.create_with_cards(self.send_request(path, params=params or None))

    def get_with_card(self, entity_id: Union[str, Entity], card_id: str, *card_field_ids: str):
        entity_id = self._get_entity_id(entity_id)
        params = {'card_field_ids': ','.join(card_field_ids)} if card_field_ids else None
        path = self._get_path(entity_id, card_id)
        return self.entity.create_with_cards(self.send_request(path, params=params))


__all__ = ['EntitiesAPI']
