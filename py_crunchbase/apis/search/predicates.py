OPERATORS = {
    'eq', 'contains', 'not_includes', 'lte', 'starts', 'domain_eq', 'gt', 'not_contains', 'not_eq', 'between',
    'gte', 'not_includes_all', 'includes', 'includes_all', 'blank', 'lt'
}


class QueryValue:
    """
    A helper class to pass simple query value
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __eq__(self, other):
        return self.evaluate() == other.evaluate()


class QueryListValue(QueryValue):
    """
    A helper class to pass list of values
    """
    def evaluate(self) -> list:
        return [value.evaluate() for value in self.value]


class Currency(QueryValue):

    def __init__(self, value: int, currency: str = 'USD'):
        super().__init__(value)
        self.currency = currency

    def evaluate(self) -> dict:
        return {'value': self.value, 'currency': self.currency}
