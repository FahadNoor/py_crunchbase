from .apis import CrunchbaseAPIException


class BaseQueryBuilder:

    Exception = CrunchbaseAPIException

    def __init__(self):
        self.fields = []
        self.order = []
        self.limit = None
        self.next_id = None
        self.previous_id = None

    def validate_fields(self, names):
        if len(names) == 0:
            raise self.Exception('Field names cannot be empty')

    def add_fields(self, names):
        self.validate_fields(names)
        self.fields.extend(names)

    def add_order(self, field: str, sort: str):
        self.order.append((field, sort))

    def add_limit(self, value: int):
        if value < 1:
            raise self.Exception(f'Invalid limit: {value}')
        self.limit = value

    def add_next(self, uuid: str):
        self.previous_id = self.next_id = None
        self.next_id = uuid

    def add_previous(self, uuid: str):
        self.previous_id = self.next_id = None
        self.previous_id = uuid
