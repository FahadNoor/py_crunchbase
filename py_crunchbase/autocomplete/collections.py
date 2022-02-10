class CollectionMeta(type):
    """
    - appends Collection._facet_name at the start of all facet values
        if _facet_name is organization then companies will become organization.companies
    - overrides __str__ for collection so that str(Collection) returns cls._name
    """

    def __new__(mcs, cls_name, bases, dict_):

        facet_name = dict_['_facet_name']
        for attr_name, value in dict_.items():
            if attr_name[0] != '_':
                dict_[attr_name] = f'{facet_name}.{value}'

        return type.__new__(mcs, cls_name, bases, dict_)

    def __str__(cls):
        return cls._name


class Collection(metaclass=CollectionMeta):

    _name = ''
    _facet_name = ''


# Below we have defined Collections to be used for AutoComplete API
# Intended use in API: str(Organizations) or str(Organizations.Companies)


class Locations(Collection):

    _name = 'locations'
    _facet_name = 'location'

    Cities = 'cities'
    Regions = 'regions'
    Countries = 'countries'
    Groups = 'groups'


class Organizations(Collection):

    _name = 'organizations'
    _facet_name = 'organization'

    Companies = 'companies'
    Investors = 'investors'
    Schools = 'schools'


class People(Collection):

    _name = 'people'
    _facet_name = 'person'

    Investors = 'investors'


class Principals(Collection):

    _name = 'principals'
    _facet_name = 'principal'

    Investors = 'investors'
