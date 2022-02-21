from typing import Union, Type

from .cards import CardsAPI
from .entities import EntitiesAPI
from ...entities import Entity


class EntitiesAPIProxy:

    def __init__(self, entity_cls: Type[Entity], api_key: str = None):
        self.entity_cls = entity_cls
        self.api_key = api_key

    def get_entities_api(self, entity_id: Union[str, Entity]) -> EntitiesAPI:
        return EntitiesAPI(entity_id=entity_id, entity_cls=self.entity_cls, api_key=self.api_key)

    def get_cards_api(self, entity_id: Union[str, Entity], card_id: str) -> CardsAPI:
        return CardsAPI(entity_id=entity_id, card_id=card_id, entity_cls=self.entity_cls, api_key=self.api_key)


__all__ = ['EntitiesAPIProxy']
