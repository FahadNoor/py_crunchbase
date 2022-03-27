from py_crunchbase.entities import Collection, Entity
from py_crunchbase.entities.key_employee_changes import KeyEmployeeChanges, KeyEmployeeChange


def test_key_employee_changes():
    assert issubclass(KeyEmployeeChanges, Collection)
    assert KeyEmployeeChanges._name == 'key_employee_changes'


def test_key_employee_change():
    assert issubclass(KeyEmployeeChange, Entity)
    assert KeyEmployeeChange.ENTITY_DEF_ID == 'key_employee_change'
    assert KeyEmployeeChange.Collection is KeyEmployeeChanges
