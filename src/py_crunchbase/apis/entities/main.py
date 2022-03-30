from itertools import chain
from typing import Union, Type, List, Iterable

from .cards import CardsAPI
from .entities_ import EntitiesAPI
from ...entities import Entity


class EntitiesAPIProxy:

    def __init__(self, entity_cls: Type[Entity], api_key: str = None):
        self.entity_cls = entity_cls
        self.api_key = api_key

    def get(
            self, entity_id: Union[str, Entity], field_ids: List[str] = None, card_ids: List[str] = None
    ) -> Entity:
        """
        returns entity with fields and card ids
        - if field_ids aren't provided, all fields are returned
        - if card_ids aren't provided, no cards are returned
        """
        api = self.get_entities_api(entity_id)

        if field_ids:
            api.select(*set(field_ids))
        else:
            api.select_all()

        if card_ids:
            api.select_cards(*set(card_ids))

        return api.execute()

    def get_cards(
            self, entity_id: Union[str, Entity], card_id: str, card_field_ids: List[str] = None,
            order_by: Union[str, Iterable] = None
    ) -> List[Entity]:
        """
        returns list of all values for given card
        """
        api = self.get_cards_api(entity_id=entity_id, card_id=card_id)
        if card_field_ids:
            api.select(*set(card_field_ids))
        if order_by:
            if isinstance(order_by, str):
                api.order_by(order_by)
            else:
                api.order_by(*order_by)
        return list(chain.from_iterable(list(entity.cards.values())[0] for entity in api.iterate()))

    def get_entities_api(self, entity_id: Union[str, Entity]) -> EntitiesAPI:
        return EntitiesAPI(entity_id=entity_id, entity_cls=self.entity_cls, api_key=self.api_key)

    def get_cards_api(self, entity_id: Union[str, Entity], card_id: str) -> CardsAPI:
        return CardsAPI(entity_id=entity_id, card_id=card_id, entity_cls=self.entity_cls, api_key=self.api_key)


__all__ = ['EntitiesAPIProxy']
