from unittest.mock import patch, call

from src.py_crunchbase.utils import is_iterable, falsy, DataDict, transform_to_data_dict


def test_is_iterable():
    class CustomObj:
        pass

    assert is_iterable('abc') is False
    assert is_iterable(['a']) is True
    assert is_iterable(('a', 'b')) is True
    assert is_iterable({'a': 'b'}) is True
    assert is_iterable(None) is False
    assert is_iterable(1) is False
    assert is_iterable(CustomObj()) is False


class TestFalsy:

    def test_bool(self):
        assert not bool(falsy)

    def test_str(self):
        assert str(falsy) == ''

    def test_getattr(self):
        assert falsy.any_attr is falsy

    def test_call(self):
        assert falsy() is falsy

    def test_getitem(self):
        assert falsy[0] is falsy
        assert falsy['a'] is falsy

    def test_contains(self):
        assert 'anything' not in falsy
        assert 1 not in falsy

    def test_len(self):
        assert len(falsy) == 0

    def test_iter(self):
        assert list(iter(falsy)) == []


def test_transform_to_data_dict():
    data = DataDict({'a': 'b'})
    assert transform_to_data_dict(data) is data

    assert transform_to_data_dict('a') == 'a'
    assert transform_to_data_dict(1) == 1
    assert transform_to_data_dict(None) is None

    data = transform_to_data_dict({'k1': 'a', 'k2': ['b'], 'k3': {'c': 'd'}})
    assert isinstance(data, DataDict)
    assert data['k1'] == 'a'
    assert data['k2'] == ['b']
    assert data['k3'] == DataDict({'c': 'd'})

    assert transform_to_data_dict(['a', 1, None, {'d': 'e'}]) == ['a', 1, None, DataDict({'d': 'e'})]


class TestDataDict:

    def test_constants(self):
        assert issubclass(DataDict, dict)

    def test_init(self):
        with patch('src.py_crunchbase.utils.transform_to_data_dict', side_effect=['v1', 'v2']) as mocked:
            data = {'a': 'A', 'b': 'B'}
            ins = DataDict(data)
            assert ins._original_data is data
            assert dict(ins) == {'a': 'v1', 'b': 'v2'}
            mocked.assert_has_calls([call('A'), call('B')])

    def test_getattr(self):
        ins = DataDict({'a': 'b'})
        assert ins.a == 'b'
        assert ins.b is falsy
