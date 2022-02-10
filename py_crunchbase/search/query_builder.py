from typing import Type

from ..base import CrunchbaseAPIException
from ..resources import Resource
from ..utils import is_iterable

OPERATORS = {
    'eq', 'contains', 'not_includes', 'lte', 'starts', 'domain_eq', 'gt', 'not_contains', 'not_eq', 'between',
    'gte', 'not_includes_all', 'includes', 'includes_all', 'blank', 'lt'
}


def convert_value(value):
    """
    given any value (str, list[str], QueryValue, list[QueryValue],
    returns a QueryListValue
    """
    if is_iterable(value):
        return QueryListValue([
            value if isinstance(value, QueryValue) else QueryValue(value)
            for value in value
        ])
    return QueryListValue([value if isinstance(value, QueryValue) else QueryValue(value)])


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


class QueryBuilder:

    ALL_FIELDS = '__All__'

    def __init__(self, resource: Type[Resource]):
        self.resource = resource
        self.fields = []
        self.queries = []
        self.order = []
        self.limit = None
        self.next_id = None
        self.previous_id = None

    def add_fields(self, names):
        if len(names) == 0:
            raise CrunchbaseAPIException('Field names cannot be empty')

        if names[0] == self.ALL_FIELDS:
            self.fields.extend(self.resource.AVAILABLE_FIELDS)
        else:
            self.fields.extend(names)

    def add_query(self, field__operator: str, value):
        try:
            field, operator = field__operator.split('__')
        except ValueError:
            raise CrunchbaseAPIException('Field and Operator should be provided in filed__operator format.')

        if operator not in OPERATORS:
            raise CrunchbaseAPIException(f'Invalid operator: {operator}')

        self.queries.append((field, operator, convert_value(value)))

    def add_order(self, field: str, sort: str):
        self.order.append((field, sort))

    def add_limit(self, value: int):
        if value < 1:
            raise CrunchbaseAPIException(f'Invalid limit: {value}')
        self.limit = value

    def add_next(self, uuid: str):
        self.previous_id = self.next_id = None
        self.next_id = uuid

    def add_previous(self, uuid: str):
        self.previous_id = self.next_id = None
        self.previous_id = uuid

    def build(self) -> dict:
        """
        returns dict to be used as query
        """
        query = {}

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

        if self.limit:
            query['limit'] = self.limit

        if self.next_id:
            query['after_id'] = self.next_id
        elif self.previous_id:
            query['before_id'] = self.previous_id

        return query
