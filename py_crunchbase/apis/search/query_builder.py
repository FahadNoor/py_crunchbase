from typing import Type

from ...entities import Entity
from ...query_builder import BaseQueryBuilder
from ...utils import is_iterable

OPERATORS = {
    'eq', 'contains', 'not_includes', 'lte', 'starts', 'domain_eq', 'gt', 'not_contains', 'not_eq', 'between',
    'gte', 'not_includes_all', 'includes', 'includes_all', 'blank', 'lt'
}


def convert_value(obj):
    """
    given any value (str, list[str], QueryValue, list[QueryValue],
    returns a QueryListValue
    """
    obj_list = obj if is_iterable(obj) else [obj]
    return QueryListValue([
        obj_ if isinstance(obj_, QueryValue) else QueryValue(obj_)
        for obj_ in obj_list
    ])


class QueryValue:
    """
    A helper class to pass simple query value
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class CurrencyValue(QueryValue):

    def __init__(self, value: int, currency: str = 'USD'):
        super().__init__(value)
        self.currency = currency

    def evaluate(self):
        return {'value': self.value, 'currency': self.currency}


class QueryListValue(QueryValue):
    """
    A helper class to pass list of values
    """
    def evaluate(self):
        return [value.evaluate() for value in self.value]


class SearchQueryBuilder(BaseQueryBuilder):

    DEFAULT_FIELDS = '__DEFAULT__'

    def __init__(self, entity_cls: Type[Entity], *args, **kwargs):
        self.entity_cls = entity_cls
        self.queries = []
        super().__init__(*args, **kwargs)

    def add_fields(self, names):
        self.validate_fields(names)

        if names[0] == self.DEFAULT_FIELDS:
            self.fields.extend(self.entity_cls.DEFAULT_FIELDS)
        else:
            self.fields.extend(names)

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
