import os.path
from collections import defaultdict
from typing import Type

from ..base import CrunchbaseAPI
from ...entities import Entity, Entities, CardType
from ...utils import DataDict


def parse_cards(cards: dict) -> DataDict:
    converted = defaultdict(list)
    for name, data_list in cards.items():
        for data in data_list:
            entity_def_id = data.get('identifier', {}).get('entity_def_id')
            try:
                entity_cls = Entities.entity_cls_by_id(entity_def_id)
            except ValueError:
                entity_cls = DataDict
            converted[name].append(entity_cls(data))
    return DataDict(converted)


class BaseEntitiesAPI(CrunchbaseAPI):

    ENTITIES_PATH = 'entities'
    CARDS_PATH = 'cards'

    def __init__(self, entity_cls: Type[Entity], api_key: str = None):
        super().__init__(api_key=api_key)
        self.entity_cls = entity_cls

    def _get_entity_id(self, entity) -> str:
        if not isinstance(entity, Entity):
            return entity
        if not isinstance(entity, self.entity_cls):
            raise self.Exception(f'Entity should be an instance of {self.entity_cls.__name__}')
        return entity.uuid or entity.identifier.permalink or ''

    def _get_path(self, entity_id: str, card_id: str = None) -> str:
        path = os.path.join(self.ENTITIES_PATH, self.entity_cls.api_path(), entity_id)
        if card_id:
            path = os.path.join(path, self.CARDS_PATH, card_id)
        return path

    def _parse_response_data(self, data: dict) -> Entity:
        entity = self.entity_cls(data.get('cards', {}).pop(CardType.fields, None) or data.get('properties', {}))
        entity.cards = parse_cards(data.get('cards', {}))
        return entity
