import os.path
from typing import Union, Type

from .base import CrunchbaseAPI
from ..entities import Entity
from ..utils import DataDict


class EntitiesAPI(CrunchbaseAPI):

    ENTITIES_PATH = 'entities'
    CARDS_PATH = 'cards'

    def __init__(self, resource: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.resource = resource

    def _get_entity_id(self, entity) -> str:
        if not isinstance(entity, Entity):
            return entity
        if not isinstance(entity, self.resource):
            raise self.Exception(f'Entity should be an instance of {self.resource.__name__}')
        return entity.uuid

    def _get_card_id(self, card) -> str:
        if isinstance(card, DataDict) and card.identifier.uuid:
            return card.identifier.uuid
        return card

    def _get_path(self, entity_id: str, card_id: str = None):
        path = os.path.join(self.ENTITIES_PATH, self.resource.API_PATH, entity_id)
        if card_id:
            path = os.path.join(path, self.CARDS_PATH, card_id)
        return path

    def get(self, entity: Union[str, Entity], *field_ids: str, card_ids: Union[list, str] = None) -> Entity:

        entity_id = self._get_entity_id(entity)
        params = {}
        if field_ids:
            params['field_ids'] = field_ids
        if card_ids:
            params['card_ids'] = card_ids

        path = self._get_path(entity_id)
        return self.resource(self.send_request(path, params=params or None))

    def get_with_card(self, entity: Union[str, Entity], card: Union[DataDict, str] = None, *card_field_ids: str):

        entity_id = self._get_entity_id(entity)
        card_id = self._get_card_id(card)
        params = {'card_field_ids': card_field_ids} if card_field_ids else None
        path = self._get_path(entity_id, card_id)
        return self.resource(self.send_request(path, params=params))


__all__ = ['EntitiesAPI']
