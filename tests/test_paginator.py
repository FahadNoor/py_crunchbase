from unittest.mock import MagicMock, patch

import pytest

from src.py_crunchbase.paginator import Paginator, Paginated


class TestPaginator:

    @pytest.fixture(name='paginator')
    def paginator_ins(self):
        return Paginator(MagicMock())

    def test_init(self):
        api = MagicMock()
        paginator = Paginator(api)
        assert paginator.api is api
        assert paginator.current_list is None

    def test_next(self, paginator):
        paginator.api.execute.side_effect = [['a'], ['b']]
        paginator.api.set_next.side_effect = [None, IndexError]
        curr_list = paginator.next()
        assert curr_list == ['a']
        assert paginator.current_list is curr_list
        paginator.api.set_next.assert_not_called()

        curr_list = paginator.next()
        assert curr_list == ['b']
        assert paginator.current_list is curr_list
        paginator.api.set_next.assert_called_once_with(['a'])

        paginator.api.set_next.reset_mock()
        with pytest.raises(StopIteration):
            paginator.next()
            paginator.api.set_next.assert_called_once_with(['b'])
    
    def test_previous(self, paginator):
        paginator.api.execute.side_effect = [['a'], ['b']]
        paginator.api.set_previous.side_effect = [None, IndexError]
        curr_list = paginator.previous()
        assert curr_list == ['a']
        assert paginator.current_list is curr_list
        paginator.api.set_previous.assert_not_called()

        curr_list = paginator.previous()
        assert curr_list == ['b']
        assert paginator.current_list is curr_list
        paginator.api.set_previous.assert_called_once_with(['a'])

        paginator.api.set_previous.reset_mock()
        with pytest.raises(StopIteration):
            paginator.previous()
            paginator.api.set_previous.assert_called_once_with(['b'])

    def test___iter__(self, paginator):
        assert paginator.__iter__() is paginator

    def test___next__(self, paginator):
        with patch.object(paginator, 'next', side_effect=[['a'], []]):
            assert paginator.__next__() == ['a']
            with pytest.raises(StopIteration):
                paginator.__next__()


class TestPaginated:

    def test_constants(self):
        assert Paginated.paginator_cls is Paginator

    def test_iterate(self):
        ins = Paginated()
        with patch.object(ins, 'paginator_cls', return_value='a') as paginator_cls:
            assert ins.iterate() == 'a'
            paginator_cls.assert_called_once_with(ins)
