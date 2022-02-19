from collections.abc import Iterable


def is_iterable(obj) -> bool:
    """
    returns true if object is iterable (False for str)
    """
    if isinstance(obj, str):
        return False
    if isinstance(obj, Iterable):
        return True
    return False


class Falsy:
    """
    It's boolean check will always be false
    Can be used as a default value
    """

    def __bool__(self):
        return False

    def __str__(self):
        return ''

    def __getattr__(self, name):
        return falsy

    def __call__(self, *args, **kwargs):
        return falsy

    def __getitem__(self, name):
        return falsy

    def __contains__(self, name):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return iter(())


def transform_to_data_dict(data):

    if isinstance(data, DataDict):
        return data

    if isinstance(data, dict):
        return DataDict({key: transform_to_data_dict(value) for key, value in data.items()})

    if is_iterable(data):
        return [transform_to_data_dict(value) for value in data]

    return data


class DataDict(dict):
    """
    This is a wrapper over dict to access values through dot annotation

    if value is a string/int, it will be returned as it is
    if value is a dict, a new DataDict will be returned with the value as data
    if value is a list, a new list will be returned with values as DataDict

    if no value is found on any given key, falsy object is returned

    Example:
        data = {
            'name': 'A company',
            'locations': ['US', 'Canada'],
            'funding': {'value': 200000, 'currency': 'US'},
            'employees': [{'name': 'John', 'role': 'CEO'}]
        }
        company = DataDict(data)
        company.name                   # 'A company'
        company.locations              # ['US', 'Canada']
        company.funding.value          # 200000
        company.employees[0].name      # 'John'

        # DataDict is a inheriting from dict class. Means it's instance can be used just like a normal dict i.e.

        company['name']                 # 'A company'
        company.get('locations')        # ['US', 'Canada']
        company.get('invalid_key')      # None

    """
    def __init__(self, data: dict):
        self._original_data = data
        data = {key: transform_to_data_dict(value) for key, value in data.items()}
        super().__init__(data)

    def __getattr__(self, name):
        return falsy if self.get(name) is None else self[name]


# singleton instance
falsy = Falsy()
