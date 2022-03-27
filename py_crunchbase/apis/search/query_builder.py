from typing import Type

from .predicates import QueryListValue, QueryValue, OPERATORS
from ...entities import Entity
from ...query_builder import BaseQueryBuilder
from ...utils import is_iterable


def convert_value(obj) -> QueryListValue:
    """
    given any value (str, list[str], QueryValue, list[QueryValue], entity, list[entity]),
    returns a QueryListValue
    """
    if isinstance(obj, Entity):
        return QueryListValue([QueryValue(obj.uuid)])

    obj_list = obj if is_iterable(obj) else [obj]
    return QueryListValue([
        obj_ if isinstance(obj_, QueryValue) else QueryValue(obj_)
        for obj_ in obj_list
    ])


class SearchQueryBuilder(BaseQueryBuilder):

    def __init__(self, entity_cls: Type[Entity], *args, **kwargs):
        self.entity_cls = entity_cls
        self.queries = []
        super().__init__(*args, **kwargs)

    def add_fields(self, names):
        self.validate_fields(names)
        self.fields = list(set(names).union(self.fields))

    def validate_fields(self, names):
        if len(names) == 0:
            raise self.Exception('Field names cannot be empty')

    def add_query(self, field__operator: str, value):
        try:
            field, operator = field__operator.split('__')
        except ValueError as exe:
            raise self.Exception(
                'Field and Operator should be provided in filed__operator format.'
            ) from exe

        if operator not in OPERATORS:
            raise self.Exception(f'Invalid operator: {operator}')

        self.queries.append((field, operator, convert_value(value)))

    def build(self) -> dict:
        """
        returns dict to be used as query
        """
        query = super().build()

        if self.fields:
            query['field_ids'] = self.fields

        if self.order:
            query['order'] = [{'field_id': field, 'sort': sort} for field, sort in self.order]

        if self.queries:
            query['query'] = [
                {
                    'type': 'predicate',
                    'field_id': field,
                    'operator_id': opr,
                    'values': value.evaluate()
                }
                for field, opr, value in self.queries
            ]

        return query
