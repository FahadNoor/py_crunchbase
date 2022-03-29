from .apis import CrunchbaseAPIException


class BaseQueryBuilder:

    Exception = CrunchbaseAPIException

    def __init__(self, min_limit: int = 1, max_limit: int = None):
        self.fields = []
        self.order = []
        self.limit = max_limit
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.next_id = None
        self.previous_id = None

    def validate_fields(self, names):
        pass

    def add_fields(self, names):
        self.validate_fields(names)
        self.fields = list(set(names).union(self.fields))

    def add_order(self, field: str, sort: str):
        self.order.append((field, sort))

    def add_limit(self, value: int):
        value = max(value, self.min_limit)
        if self.max_limit:
            value = min(value, self.max_limit)
        self.limit = value

    def add_next(self, uuid: str):
        self.previous_id = None
        self.next_id = uuid

    def add_previous(self, uuid: str):
        self.next_id = None
        self.previous_id = uuid

    def build(self) -> dict:
        params = {}

        if self.next_id:
            params['after_id'] = self.next_id
        if self.previous_id:
            params['before_id'] = self.previous_id
        if self.limit:
            params['limit'] = self.limit

        return params
