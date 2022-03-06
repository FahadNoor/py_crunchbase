from .base import Entity, Collection


class KeyEmployeeChanges(Collection):

    _name = 'key_employee_changes'


class KeyEmployeeChange(Entity):

    ENTITY_DEF_ID = 'key_employee_change'
    Collection = KeyEmployeeChanges
